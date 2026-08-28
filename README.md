# 대상종합공사 랜딩페이지

대전·세종·충청 전역에서 우수관·트렌치·렉산·방수·동파방지 열선·태양광 가로등·벌목 등을
시공하는 대상종합공사의 원페이지 소개 사이트입니다.

문의: **010-3996-6004** · 블로그: <https://blog.naver.com/zipsuridoc>

## 구조

```
index.html          배포되는 페이지 (약 77 KB, 빌드 산출물이라 직접 고치지 않음)
img/                시공 사진 26장 (약 2.7 MB)
src/template.html   실제로 편집하는 원본 — 사진은 {{img:이름}} 으로 참조
src/build.py        template.html → index.html + dist/single.html
vercel.json         이미지 캐시 및 보안 헤더
robots.txt
```

## 수정하는 법

1. `src/template.html` 을 고친다. (`index.html` 을 직접 고치면 다음 빌드에서 덮어써짐)
2. 아래 명령으로 다시 빌드한다.

```bash
python src/build.py
```

두 가지가 만들어집니다.

| 파일 | 크기 | 용도 |
|---|---|---|
| `index.html` | 약 77 KB | 배포용. 사진을 `/img/` 에서 따로 불러오므로 화면이 먼저 뜨고 사진이 뒤따라 들어옴 |
| `dist/single.html` | 약 3.6 MB | 사진까지 전부 파일 하나에 넣은 버전. 서버 없이 파일만 열면 되는 상황용 (git 에는 올리지 않음) |

사진을 추가하려면 `img/` 에 `이름.jpg` 로 넣고 템플릿에서 `{{img:이름}}` 으로 부르면 됩니다.

## 배포 (Vercel)

빌드 과정이 없는 정적 사이트라 별도 설정이 필요 없습니다.

- Framework Preset: **Other**
- Build Command: 비움
- Output Directory: 비움 (저장소 루트)

`main` 브랜치에 푸시하면 자동으로 다시 배포됩니다.

### 도메인 연결 후 한 가지

링크를 카카오톡·페이스북에 붙였을 때 뜨는 미리보기 이미지 주소는 절대경로여야 합니다.
도메인이 정해지면 그 주소로 한 번 빌드해 주세요.

```bash
SITE_URL=https://실제도메인 python src/build.py
```

윈도우 PowerShell 에서는:

```powershell
$env:SITE_URL="https://실제도메인"; python src/build.py
```

## 사진 출처

모든 사진은 대상종합공사 네이버 블로그(<https://blog.naver.com/zipsuridoc>)에 공개된
실제 시공 현장 사진입니다. 통계로 표기한 수치도 블로그에 공개된 시공 기록에서 집계했습니다.
