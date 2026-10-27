# S-LINK 2.0

**OSや機器の違いを越えて、センサーやモーターを活用するための共通通信規格です。**  
**A common communication standard for using sensors and motors across different operating systems and devices.**

[S-LINK 公式サイト / Official website](https://s-link.education/)

## 日本語

S-LINKは、教育用フィジカルコンピューティングにおいて、メーカーの異なる機器とソフトウェアを共通の通信方式で接続するための規格です。ハードウェアとソフトウェアの選択肢を広げ、教育現場での利用や教材開発を容易にすることを目指しています。

### 公開資料

現在の文書の版: **0.1（DRAFT、2026-10-27）**。版の一覧は[Releases](https://github.com/s-link/s-link-spec/releases)をご覧ください。文書の版は、通信上の版番号（S-LINK 2.0、機能表の版 1）とは独立しています。

| ファイル | 内容 |
|---|---|
| [S-LINK 2.0 規格書](S-LINK2.0/S-LINK2.0-規格書.md) | S-LINKの通信部分を実装するための仕様 |
| [S-LINK 2.0 機能表](S-LINK2.0/S-LINK2.0-機能表.md) | 各機能の番号、単位、データ形式、動作 |
| [規格書・機能表 DRAFT PDF](S-LINK2.0/S-LINK2.0-規格書・機能表.pdf) | 2文書をまとめた閲覧用PDF。生成元の版（タグ）を記載 |

### S-LINK対応について

S-LINK対応は、実装された機能について共通の通信仕様に従うことを意味します。すべてのS-LINK対応ソフトウェアが、すべての対応デバイスで動作することを保証するものではありません。ソフトウェアや教材の提供者は、対応するデバイスを指定できます。

### ライセンス

このリポジトリの内容（規格書、機能表、PDF）は、[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/deed.ja)で公開します。商用・非商用を問わず、複製・改変・再配布できます。出典表示は義務ではありませんが、歓迎します。詳しくは[LICENSE](LICENSE)をご覧ください。

S-LINKを利用するライブラリ（JavaScript、Pythonなど）は、このリポジトリとは別に公開します。それぞれのライセンスは、各リポジトリに記載します。

CC0は、商標権および特許権を許諾の対象としていません。

### 名称・ロゴについて

製品やソフトウェアがこの規格に対応していることを説明するために、「S-LINK」の名称を用いることは自由です。許可は必要ありません。

S-LINKのロゴ、および認証を示すマークは、上記のライセンスの対象ではありません。利用条件は別途定めます。

### 提案・報告

誤記、仕様の不明点、実装上の問題、改善の提案は、Issueで受け付けます。通信仕様の変更は、既存の対応製品やソフトウェアとの互換性への影響を確認したうえで判断します。詳しくは[CONTRIBUTING.md](CONTRIBUTING.md)をご覧ください。

### 運営

S-LINKは、株式会社ティーファブワークスがAkaDakoの開発過程で考案しました。現在、仕様の公開と管理は同社が行っています。今後、複数のメーカーや教育関係者が参加する運営体制への移行を予定しており、決まり次第このリポジトリで案内します。

---

## English

S-LINK is a communication standard intended to connect educational physical-computing devices and software from different manufacturers through a common protocol. It aims to broaden hardware and software choices and make classroom use and educational content development easier.

### Published documents

Current document revision: **0.1 (DRAFT, 2026-10-27)**. See [Releases](https://github.com/s-link/s-link-spec/releases) for all revisions. The document revision is independent of the protocol version numbers (S-LINK 2.0, function table revision 1).

| File | Description |
|---|---|
| [S-LINK 2.0 Specification](S-LINK2.0/S-LINK2.0-規格書.md) | Protocol specification for implementing S-LINK communications |
| [S-LINK 2.0 Function Table](S-LINK2.0/S-LINK2.0-機能表.md) | Function identifiers, units, data formats, and behavior |
| [Specification and Function Table, DRAFT PDF](S-LINK2.0/S-LINK2.0-規格書・機能表.pdf) | Both documents combined for reading. The source revision (tag) is noted inside |

### What S-LINK compatibility means

S-LINK compatibility means following the common communication specification for the functions implemented by a device. It does **not** guarantee that every S-LINK-compatible application will work with every S-LINK-compatible device. Software and educational content providers may specify which devices they support.

### License

The contents of this repository (the specification, the function table, and the PDF) are published under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/). Copying, modification, and redistribution are permitted, including for commercial purposes. Attribution is appreciated but not required. See [LICENSE](LICENSE) for details.

Libraries that use S-LINK (JavaScript, Python, and others) are published in separate repositories. Each repository states its own license.

CC0 does not grant trademark or patent rights.

### Name and logo

You may use the name "S-LINK" to state that a product or software supports this specification. No permission is required.

The S-LINK logo and certification marks are not covered by the license above. Terms for their use will be provided separately.

### Proposals and reports

Typos, unclear points in the specification, implementation issues, and improvement proposals are welcome through Issues. Changes to the communication specification are decided after reviewing their impact on compatibility with existing devices and software. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Governance

S-LINK was designed by TFabWorks during the development of AkaDako. TFabWorks currently publishes and maintains the specification. A transition to a governance structure with multiple manufacturers and education stakeholders is planned, and will be announced in this repository once decided.
