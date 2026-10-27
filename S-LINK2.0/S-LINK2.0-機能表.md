# S-LINK 2.0 機能表

| 項目 | 内容 |
|---|---|
| 文書の版 | 0.1（DRAFT） |
| 発行日 | 2026-10-27 |
| 機能表の版（`function_table_revision`） | 1 |

文書の版は、この機能表の文章の改訂を示す番号です。`HELLO` が返す `function_table_revision` とは独立しています。

機能表では、機能番号ごとに単位、データ形式、動作を定めます。
メッセージのバイト構成とホスト・デバイスの動作は、[S-LINK 2.0 規格書](S-LINK2.0-規格書.md) が定めます。

入力・出力は、デバイスを基準とします。ホストは入力機能の値を読み取り、出力機能に値を書き込みます。
`access` の `read` は入力機能、`write` は出力機能を表します。

- 機能番号は U14
- 指数はチャンネルごとに `CAPABILITY` の `exponent` が宣言する
- 版は 1。`HELLO` が返す `function_table_revision` はこの値

```
機能   61 件（入力 48 / 出力 13）
```

---

## ※ 指数・値域・分解能

指数（例）・値域・分解能の各欄は参考情報です。値域欄には、`payload` 型で表せる範囲または機能上の範囲を示します。機能として受け付ける範囲は、各機能の説明欄で定めます。ホストは送受信する値を、チャンネルごとの `CAPABILITY` の `exponent` で解釈します。
同じ `RESIST` でも、mΩ 計は `−5`、MΩ 計は `−1` を宣言します。

## `payload` 列の読み方

この表の `payload` は、`READ` のレスポンスや `WRITE` で扱う値の部分です。符号化後の上限は 61 byte です。メッセージの `payload_length` は、この値に `transaction_id`、`function_id`、`port` の計 5 byte を加えた長さを表します（上限 66 byte）。長さフィールド自体は含めません。

`payload` の読み方、型、指数の適用方法は[規格書 6.3](S-LINK2.0-規格書.md#63-機能表の項目)を参照してください。

---

## 機能番号の範囲

| 範囲 | 用途 | 説明 |
|---|---|---|
| `0x0100–0x3DFF` | 正式な機能 | 機能表に掲載する機能に割り当てる |
| `0x3E00–0x3EFF` | 非公式の機能番号 | 機器の開発者が独自の機能に割り当てる |
| `0x3F00–0x3FFE` | 予約 | 機能には割り当てない |
| `0x3FFF` | 該当なし | 機能に対応する番号がないことを示す |

非公式の機能番号 `0x3E00`–`0x3EFF` は、同じ番号が機種ごとに異なる機能を表すことがあります。ホストは対象の接続で得た `model_id` と機器の説明書を確認してから解釈します。別の接続の `model_id` や値の定義を流用しません。

独自機能も `CAPABILITY` で宣言し、既存の `READ` / `WRITE` 形式、データ型、長さ上限、応答と状態管理に従います。値の意味・型・長さ・範囲などは機器の説明書が定めます。

通信手順は、[規格書 6.4](S-LINK2.0-規格書.md#64-非公式の機能番号)を参照してください。

## 生の値

| `function_id` | `name` | 表示名 | English | `access` | `kind` | 単位 | `payload` | 指数（例）※ | 値域 ※ | 分解能 ※ | 説明 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `0x0100` | `DIGITAL_IN` | デジタル入力 | Digital input | `read` | `boolean` | — | value U7 | 0 | 0 / 1 | — | 端子の電圧が Low か High か。スイッチやデジタル出力センサーの値を読み取る |
| `0x0101` | `DIGITAL_IN_PU` | デジタル入力（プルアップ） | Digital input, pull-up | `read` | `boolean` | — | value U7 | 0 | 0 / 1 | — | 内蔵のプルアップ抵抗を有効にして読み取る。スイッチを 2 本の線だけで接続できる |
| `0x0102` | `ANALOG_IN` | アナログ入力 | Analog input | `read` | `adc` | — | value U28 | 0 | 0 – 268,435,455 | 1 カウント | 端子の電圧をアナログ・デジタル（A/D）変換し、A/D 値を返す。自作センサーや、ホスト側で独自に換算する素子に使う |

## 電気・磁気・時間

| `function_id` | `name` | 表示名 | English | `access` | `kind` | 単位 | `payload` | 指数（例）※ | 値域 ※ | 分解能 ※ | 説明 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `0x0200` | `VOLT` | 電圧 | Voltage | `read` | `quantity` | V | value S28 | −3 | ±134,217.727 V | 1 mV | その瞬間の電圧。符号つき。直流回路や、READ を繰り返して行う波形観測に使う |
| `0x0201` | `VOLT_RMS` | 電圧（実効値） | Root mean square voltage | `read` | `quantity` | V | value U28 | −3 | 0 – 268,435.455 V | 1 mV | 電圧の実効値。交流の測定に使う |
| `0x0202` | `CURRENT` | 電流 | Current | `read` | `quantity` | A | value S28 | −6 | ±134.217727 A | 1 µA | その瞬間の電流。符号つき。オームの法則に使う |
| `0x0203` | `CURRENT_RMS` | 電流（実効値） | Root mean square current | `read` | `quantity` | A | value U28 | −6 | 0 – 268.435455 A | 1 µA | 電流の実効値。クランプメーターはこれを返す |
| `0x0204` | `RESIST` | 抵抗 | Resistance | `read` | `quantity` | ohm | value U28 | −2 | 0 – 2,684,354.55 Ω | 0.01 Ω | 抵抗。電熱線や直列並列の合成抵抗に使う |
| `0x0205` | `CAP` | 静電容量 | Capacitance | `read` | `quantity` | F | value U28 | −10 | 0 – 0.0268435455 F | 100 pF | 静電容量。コンデンサーの容量測定や、抵抗を使った放電特性の確認に使う |
| `0x0206` | `IND` | インダクタンス | Inductance | `read` | `quantity` | H | value U28 | −7 | 0 – 26.8435455 H | 0.1 µH | インダクタンス。自己誘導や、コイルとコンデンサーで構成する共振回路の測定に使う |
| `0x0207` | `POWER` | 電力 | Power | `read` | `quantity` | W | value S28 | −3 | ±134,217.727 W | 1 mW | 電力。符号つき。発電設備や電気機器の出力測定に使う |
| `0x0208` | `ENERGY` | 電力量 | Energy | `read` | `quantity` | J | value S28 | −1 | ±13,421,772.7 J | 0.1 J | 電力量。電源投入時を 0 とする累積量。充電で増え、放電で減る |
| `0x0209` | `EFIELD` | 電界 | Electric field | `read` | `quantity` | V/m | value S28 | −1 | ±13,421,772.7 V/m | 0.1 V/m | 測定軸方向の電界。正の向きは機器の説明書が定める |
| `0x020A` | `MAG` | 磁束密度 | Magnetic flux density | `read` | `quantity` | T | x / y / z S28 | −8 | ±1.34217727 T | 10 nT | 3 軸の磁束密度。x / y / z のすべてに同じ exponent を適用する |
| `0x020B` | `FREQ` | 周波数 | Frequency | `read` | `quantity` | Hz | value U28 | −2 | 0 – 2,684,354.55 Hz | 0.01 Hz | 周波数。音の高さや交流の測定に使う |
| `0x020C` | `GATE_TIME` | 通過時間 | Gate time | `read` | `quantity` | s | duration U28 / count U14 | −6 | 0 – 268.435455 s / 0 – 16,383 | 1 µs | 光電ゲートなどで、ゲートが遮られていた時間を測る。READ は最後に終了した測定の duration と累積 count を返す。count は遮られた回数で、exponent を適用しない。電源投入時は 0 とし、遮られるたびに 1 増やす。16,383 の次は 0 に戻る |

## 環境

| `function_id` | `name` | 表示名 | English | `access` | `kind` | 単位 | `payload` | 指数（例）※ | 値域 ※ | 分解能 ※ | 説明 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `0x0300` | `ILLUM` | 明るさ | Illuminance | `read` | `quantity` | lx | value U28 | −2 | 0 – 2,684,354.55 lx | 0.01 lx | 人の目の感度で重み付けした明るさ。日なたと日かげの比較に使う |
| `0x0301` | `UV` | 紫外線 | Ultraviolet index | `read` | `quantity` | 1 | value U14 | −1 | 0 – 1,638.3 | 0.1 | 国際照明委員会（CIE）の紅斑作用スペクトルに基づき、国際標準化機構（ISO）の規格 17166 に従って重み付けした紫外線の放射照度を、25 mW/m² で割った値 |
| `0x0302` | `WAVELENGTH` | 波長 | Wavelength | `read` | `quantity` | nm | value U14 | −1 | 0 – 1,638.3 nm | 0.1 nm | 最も強い成分の波長。回折格子を使った発光スペクトルの測定などに使う |
| `0x0303` | `REFRACT` | 屈折率 | Refractive index | `read` | `quantity` | 1 | value U28 | −5 | 0 – 2,684.35455 | 0.00001 | 屈折率。光の屈折のほか、濃度や純度の測定にも使う |
| `0x0304` | `TEMP` | 温度 | Temperature | `read` | `quantity` | degC | value S28 | −2 | ±1,342,177.27 ℃ | 0.01 ℃ | 温度 |
| `0x0305` | `HUMID` | 湿度 | Humidity | `read` | `quantity` | percentRH | value U14 | −2 | 0 – 163.83 %RH | 0.01 %RH | 相対湿度（%RH）。気温と組み合わせた環境監視に使う |
| `0x0306` | `PRESS` | 気圧 | Pressure | `read` | `quantity` | hPa | value U28 | −2 | 0 – 2,684,354.55 hPa | 0.01 hPa | 大気圧。高度による変化や、天気の移り変わりを追う |
| `0x0307` | `DIFF_PRESS` | 差圧 | Differential pressure | `read` | `quantity` | hPa | value S28 | −4 | ±13,421.7727 hPa | 0.0001 hPa | 2 つの圧力口の圧力差。ベルヌーイの定理やピトー管を使った測定に使う |
| `0x0308` | `CO2` | 二酸化炭素 | Carbon dioxide | `read` | `quantity` | ppm | value U28 | 0 | 0 – 268,435,455 ppm | 1 ppm | 二酸化炭素の濃度。呼吸・燃焼・光合成などに伴う濃度変化の測定に使う |
| `0x0309` | `O2` | 酸素 | Oxygen | `read` | `quantity` | percent | value U14 | −2 | 0 – 163.83 % | 0.01 % | 酸素の体積分率。燃焼などに伴う酸素濃度の変化を測る |
| `0x030A` | `PH` | pH | pH | `read` | `quantity` | 1 | value U14 | −2 | 0 – 163.83 | 0.01 | 水溶液の酸性・アルカリ性を表す。滴定や水質管理などに使う |
| `0x030B` | `ORP` | 酸化還元電位 | Redox potential | `read` | `quantity` | V | value S28 | −4 | ±13,421.7727 V | 0.1 mV | 参照電極を基準とする電位。標準水素電極への換算の要否は機器の説明書が定める |
| `0x030C` | `DO` | 溶存酸素 | Dissolved oxygen | `read` | `quantity` | mg/L | value U14 | −2 | 0 – 163.83 mg/L | 0.01 mg/L | 水に溶けている酸素の量。水質評価や、生物の呼吸・光合成に伴う変化の把握に使う |
| `0x030D` | `TURB` | 濁度 | Turbidity | `read` | `quantity` | FNU | value U14 | −1 | 0 – 1,638.3 FNU | 0.1 FNU | 860 nm・90° 散乱で測った濁り（国際標準化機構（ISO）の規格 7027-1）。FNU（ホルマジン比濁単位）で表す。ろ過や川の水の観察に使う |
| `0x030E` | `EC` | 導電率 | Conductivity | `read` | `quantity` | S/m | value U28 | −4 | 0 – 26,843.5455 S/m | 0.0001 S/m | 電気の通しやすさ（導電率）。25 ℃ 換算かどうかは機器の説明書が定める |

## 力学・運動

| `function_id` | `name` | 表示名 | English | `access` | `kind` | 単位 | `payload` | 指数（例）※ | 値域 ※ | 分解能 ※ | 説明 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `0x0400` | `DIST` | 距離 | Distance | `read` | `quantity` | mm | value U28 | −1 | 0 – 26,843,545.5 mm | 0.1 mm | 対象までの距離。物体の位置や動きの測定に使う |
| `0x0401` | `DISP` | 変位 | Displacement | `read` | `quantity` | mm | value S28 | −2 | ±1,342,177.27 mm | 0.01 mm | 基準位置からの符号つきのずれ。単振動やばね振り子に使う |
| `0x0402` | `SPEED` | 速度 | Velocity | `read` | `quantity` | m/s | value S28 | −3 | ±134,217.727 m/s | 1 mm/s | 測定軸の向きを正とする速度の成分。力学台車や走行ロボットに使う |
| `0x0403` | `ACCEL` | 加速度 | Acceleration | `read` | `quantity` | m/s2 | x / y / z S28 | −4 | ±13,421.7727 m/s² | 0.0001 m/s² | 3 軸の加速度。x / y / z のすべてに同じ exponent を適用する。傾き・振動・落下の測定に使う |
| `0x0404` | `GYRO` | 角速度 | Angular rate | `read` | `quantity` | deg/s | x / y / z S28 | −2 | ±1,342,177.27 deg/s | 0.01 deg/s | 3 軸の角速度。x / y / z のすべてに同じ exponent を適用する。回転運動やロボットの姿勢に使う |
| `0x0405` | `ANG_ACCEL` | 角加速度 | Angular acceleration | `read` | `quantity` | deg/s2 | x / y / z S28 | −1 | ±13,421,772.7 deg/s² | 0.1 deg/s² | 3 軸の角加速度。x / y / z のすべてに同じ exponent を適用する。回転速度の変化や、回転運動の解析に使う |
| `0x0406` | `FORCE` | 力 | Force | `read` | `quantity` | N | value S28 | −3 | ±134,217.727 N | 1 mN | 力。符号つき。ばねの伸び、浮力、摩擦力などの測定に使う |
| `0x0407` | `TORQUE` | トルク | Torque | `read` | `quantity` | N·m | value S28 | −4 | ±13,421.7727 N·m | 0.1 mN·m | 回転させる力。回転体のつり合いや慣性モーメントの評価に使う |
| `0x0408` | `STRAIN` | ひずみ | Strain | `read` | `quantity` | 1 | value S28 | −7 | ±13.4217727 | 0.0000001 | ひずみ（ΔL/L）。材料の弾性や変形の評価に使う |
| `0x0409` | `MASS` | 質量 | Mass | `read` | `quantity` | kg | value S28 | −6 | ±134.217727 kg | 1 mg | 質量。符号つき。反応や溶解に伴う質量変化の測定に使う |
| `0x040A` | `ENCODER` | 回転量 | Rotation | `read` | `quantity` | deg | value S28 | −1 | ±13,421,772.7 deg | 0.1 deg | 軸の回転量。電源投入時を 0 とする累積量。負で逆回転 |

## 検知・操作・生体

| `function_id` | `name` | 表示名 | English | `access` | `kind` | 単位 | `payload` | 指数（例）※ | 値域 ※ | 分解能 ※ | 説明 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `0x0500` | `BUTTON` | ボタン | Button | `read` | `boolean` | — | value U7 | 0 | 0 / 1 | — | ボタンが押されているか。負論理の配線でも 1 が「押している」 |
| `0x0501` | `POT` | つまみの位置 | Potentiometer | `read` | `quantity` | percent | value U14 | −2 | 0 – 100 % | 0.01 % | つまみの位置。一方の端が 0 %、もう一方の端が 100 % |
| `0x0502` | `PIR` | 人の検知 | Passive infrared motion detection | `read` | `boolean` | — | value U7 | 0 | 0 / 1 | — | 人が動いたかどうか。焦電センサーの出力をそのまま返す |
| `0x0503` | `PROXIMITY` | 近接 | Proximity | `read` | `boolean` | — | value U7 | 0 | 0 / 1 | — | 物体に触れずに、その有無を検出する。自動ドアなどに使う |
| `0x0504` | `MAGNET_NEAR` | 磁気近接 | Magnet proximity | `read` | `boolean` | — | value U7 | 0 | 0 / 1 | — | 磁石が近いことを検知する。リードスイッチを使った開閉検出や、磁石の性質の観察に使う |
| `0x0505` | `HEART` | 心拍 | Heart rate | `read` | `quantity` | bpm | value U14 | 0 | 0 – 16,383 bpm | 1 bpm | 心拍数 |

## 出力機能

| `function_id` | `name` | 表示名 | English | `access` | `kind` | 単位 | `payload` | 指数（例）※ | 値域 ※ | 分解能 ※ | 説明 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `0x1000` | `LEVEL` | 出力の強さ | Output level | `write` | `quantity` | percent | value U14 | −2 | 0 – 100 % | 0.01 % | 端子の出力を 0〜100 % で駆動する。on/off も 0 % と 100 % で表す |
| `0x1001` | `SERVO` | サーボモーター | Servo motor | `write` | `quantity` | deg | angle U14 | −1 | 0 – 180 deg | 0.1 deg | サーボモーターの軸を指定した角度（0〜180 度）に動かす |
| `0x1002` | `VOLT_OUT` | 電圧を出す | Voltage output | `write` | `quantity` | V | value S28 | −3 | ±134,217.727 V | 1 mV | 指定した電圧を出す。計装の 0–10 V や D/A 変換に使う |
| `0x1003` | `RELAY` | 制御スイッチ（リレー） | Relay | `write` | `boolean` | — | value U7 | 0 | 0 / 1 | — | 接点を開閉する |
| `0x1004` | `MOTOR` | モーター | Motor | `write` | `quantity` | percent | value S28 | −2 | −100 – 100 % | 0.01 % | 出力を −100〜100 % で駆動する。負で逆転 |
| `0x1005` | `PUMP` | ポンプ | Pump | `write` | `quantity` | percent | value U14 | −2 | 0 – 100 % | 0.01 % | 出力を 0〜100 % で駆動する |
| `0x1006` | `FAN` | 送風 | Fan | `write` | `quantity` | percent | value U14 | −2 | 0 – 100 % | 0.01 % | 出力を 0〜100 % で駆動する |
| `0x1007` | `VIBRATOR` | 振動 | Vibration | `write` | `quantity` | percent | value U14 | −2 | 0 – 100 % | 0.01 % | 出力を 0〜100 % で駆動する |
| `0x1008` | `ELECTROMAG` | 電磁石 | Electromagnet | `write` | `quantity` | percent | value U14 | −2 | 0 – 100 % | 0.01 % | 出力を 0〜100 % で駆動する |
| `0x1009` | `SOLENOID` | 押し出し | Solenoid | `write` | `boolean` | — | value U7 | 0 | 0 / 1 | — | 0 = 戻す、1 = 押す |
| `0x100A` | `STEPPER` | ステッピングモーター | Stepper | `write` | `quantity` | deg | angle S28 / speed U14 | −1 | 角度 ±13,421,772.7 deg / 速度 0 – 16,383 deg/s | 0.1 deg | 目標角度と、その位置まで移動する速度。原点は電源投入時の位置。PORT_RELEASE でそのときの位置が新しい原点になる。speed は deg/s の整数で、exponent は適用しない。0 はデバイスの既定の速さ |
| `0x100B` | `RGB` | フルカラー LED | RGB LED | `write` | `color` | — | index U14 / r / g / b U7 | 0 | index 0 – 16,383、各成分 0 – 127 | 1 | `index` 番目の LED の赤（R）・緑（G）・青（B）を指定する。各成分は 7 bit で、127 が最大値。0–255 の RGB 値を使う場合は、各成分を 1 bit 右へずらす（255 → 127）。LED 数以上の `index` には `ERROR(BAD_REQUEST)` を返す |
| `0x100C` | `HEATER` | 加熱・冷却 | Heater / cooler | `write` | `quantity` | percent | value S28 | −2 | −100 – 100 % | 0.01 % | 出力を −100〜100 % で駆動する。負の値はペルチェ素子による冷却を表す |

## `boolean` の値の意味

| `function_id` | 0 | 1 |
|---|---|---|
| `0x0100 DIGITAL_IN / 0x0101 DIGITAL_IN_PU` | Low | High |
| `0x0500 BUTTON` | 離している | 押している |
| `0x0502 PIR` | 検知なし | 検知あり |
| `0x0503 PROXIMITY` | 物なし | 物あり |
| `0x0504 MAGNET_NEAR` | 磁石なし | 磁石あり |
| `0x1003 RELAY` | 開く | 閉じる |
| `0x1009 SOLENOID` | 戻す | 押す |
