# S-LINKへの提案・報告 / Proposals and reports for S-LINK

> **Language / 言語:** 日本語と英語を併記します。内容に差異がある場合は、管理者が意図を確認します。 / Japanese and English are provided together. If the two versions differ, maintainers will clarify the intended meaning.

## 日本語

### 1. Issueで受け付けるもの

次の内容は、Issueで受け付けます。

- 誤字脱字、リンク切れ、説明のわかりにくい箇所
- 仕様の曖昧な点、解釈が分かれる動作、エラー条件の不明点
- 実装してわかった問題（できれば、機器名、ホスト環境、再現手順を添えてください）
- 機能や仕様変更の提案（目的、想定する使い方、既存の対応製品への影響を書いてください）

機密情報、第三者の非公開資料、個人情報は投稿しないでください。公開の場に書けない内容は、[公式サイト](https://s-link.education/)の連絡先からご相談ください。

### 2. Pull Requestについて

仕様書本文へのPull Requestの受け入れ条件（貢献部分の権利の扱いを含む）は、現在整備中です。整備でき次第、この文書を更新します。

それまでの間、修正や変更の提案はIssueでお知らせください。管理者が内容を確認し、仕様書に反映します。Issueを経ずに送られたPull Requestは、確認のうえ、Issueでの相談をお願いすることがあります。

### 3. 仕様変更の考え方

S-LINKは教育現場での安定した運用を重視します。通信仕様の変更は、既存の対応製品、ライブラリ、教材への影響と移行方法を確認したうえで判断します。互換性を損なう変更は慎重に扱い、採用する場合は移行期間や互換性の方針をあわせて示します。

仕様書の更新と、正式な版の発行は別です。正式な版とその公開日は、リポジトリのリリース情報等で明示します。

### 4. 運営

現在、仕様の公開と管理、Issueの確認は、株式会社ティーファブワークスが行っています。運営体制に変更がある場合は、このリポジトリで案内し、この文書を更新します。

---

## English

### 1. What to report through Issues

The following are welcome as Issues:

- Typos, broken links, and unclear explanations
- Ambiguities in the specification, behavior open to interpretation, and unclear error conditions
- Problems found during implementation (please include the device, host environment, and steps to reproduce where possible)
- Proposals for features or specification changes (please describe the purpose, intended use, and impact on existing compatible products)

Do not submit confidential information, unpublished third-party materials, or personal information. For matters that cannot be discussed publicly, please use the contact details on the [official website](https://s-link.education/).

### 2. Pull Requests

The conditions for accepting Pull Requests to the specification text, including how rights in contributed material are handled, are still being prepared. This document will be updated once they are in place.

Until then, please submit corrections and proposed changes as Issues. Maintainers will review them and update the specification. Pull Requests submitted without a prior Issue may be reviewed and redirected to an Issue.

### 3. Approach to specification changes

S-LINK prioritizes stable use in educational settings. Changes to the communication specification are decided after reviewing their impact on existing compatible products, libraries, and learning materials, and how migration would work. Changes that affect compatibility are treated cautiously; if adopted, a transition period and compatibility policy will be provided.

Updating the specification text and publishing an official version are separate steps. Official versions and their release dates are identified in repository releases or equivalent notices.

### 4. Governance

TFabWorks currently publishes and maintains the specification and reviews Issues. Changes to the governance structure will be announced in this repository, and this document will be updated accordingly.
