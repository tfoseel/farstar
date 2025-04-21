# 🌌 FarStar - 감성 별자리 SNS API

FarStar는 별을 중심으로 감정을 기록하고 공유하는, 감성 기반 SNS 프로젝트입니다.
사용자의 현재 위치와 시간을 기준으로 하늘에 보이는 별에만 글을 쓸 수 있으며,
하늘 위에 떠 있는 별을 통해서만 게시물을 읽을 수 있는 새로운 형태의 글쓰기 경험을 제공합니다.

👉 [FarStar 프로젝트 아이디어 노트](https://velog.io/@smilelee9/%EC%95%84%EC%9D%B4%EB%94%94%EC%96%B4-%EB%85%B8%ED%8A%B8-%EB%B3%84%EC%9E%90%EB%A6%AC-%EA%B0%90%EC%84%B1-SNS-%EC%95%B1-farStar)

---

## 🔗 Base URL

```
http://localhost:8000/api/
```


---

## 🔐 1. 인증 (Authentication)

| 메서드     | URL                    | 설명                             |
| ------- | ---------------------- | ------------------------------ |
| `POST`  | `/auth/register/`      | 회원가입                           |
| `POST`  | `/auth/login/`         | JWT 로그인 (access/refresh 토큰 발급) |
| `POST`  | `/auth/token/refresh/` | access 토큰 재발급                  |
| `GET`   | `/auth/profile/`       | 내 프로필 조회                       |
| `PATCH` | `/auth/profile/`       | 내 프로필 수정                       |
| `GET`   | `/auth/posts/`         | 내가 작성한 글 목록 조회                 |

---

## ✍️ 2. 게시물 (Posts)

| 메서드      | URL                             | 설명                       |
| -------- | ------------------------------- | ------------------------ |
| `POST`   | `/posts/`                       | 글 작성 (위치 기반 별이 보일 때만 가능) |
| `GET`    | `/posts/list/`                  | 로그인한 사용자의 전체 글 목록        |
| `DELETE` | `/posts/<id>/`                  | 글 삭제                     |
| `POST`   | `/posts/<id>/check-visibility/` | 특정 글의 현재 가시성 확인 (위치 기반)  |

---

## 🌟 3. 별 (Stars)

| 메서드   | URL                                                 | 설명                                     |
| ----- | --------------------------------------------------- | -------------------------------------- |
| `GET` | `/stars/<id>/posts/?latitude=<lat>&longitude=<lon>` | 해당 별의 게시물 목록 (현재 위치에서 별이 하늘에 있을 때만 응답) |

---

## 🔮 4. 별자리 (Constellations)

> 🛠️ **미구현 - 예정된 기능**

| 메서드    | URL                       | 설명                   |
| ------ | ------------------------- | -------------------- |
| `GET`  | `/constellations/`        | 별자리 전체 목록            |
| `GET`  | `/constellations/<id>/`   | 별자리 상세 정보            |
| `POST` | `/constellations/unlock/` | 별자리 해금 (Lumen 또는 결제) |
| `POST` | `/constellations/custom/` | 커스텀 별자리 생성           |

---

## 💰 5. Lumen 시스템

> 🛠️ **미구현 - 예정된 기능**

| 메서드    | URL                    | 설명              |
| ------ | ---------------------- | --------------- |
| `GET`  | `/lumen/balance/`      | 내 Lumen 잔액 확인   |
| `GET`  | `/lumen/transactions/` | Lumen 획득/소비 이력  |
| `POST` | `/lumen/earn/`         | 출석체크 등 활동 기반 보상 |
| `POST` | `/lumen/spend/`        | 별자리 해금 등에 사용    |

---

## 💳 6. Stripe 결제 (Payments)

> 🛠️ **미구현 - 예정된 기능**

| 메서드    | URL                   | 설명                    |
| ------ | --------------------- | --------------------- |
| `POST` | `/payments/checkout/` | Stripe Checkout 세션 생성 |
| `POST` | `/payments/webhook/`  | Stripe Webhook 처리     |
| `GET`  | `/payments/history/`  | 결제 내역 조회              |

---

## 🌍 위치 기반 요청 안내

아래 API는 요청 시 `latitude`, `longitude` 쿼리 파라미터 또는 body 필드가 필요합니다:

- `POST /posts/` → 글 작성
- `GET /stars/<id>/posts/` → 별의 게시물 목록 조회
- `POST /posts/<id>/check-visibility/` → 별이 현재 보이는지 확인

---

## 🚀 향후 계획

- Skyfield 연동 별자리 활성화 기능 자동화
- 사용자 경험 기반 힐링 퀘스트
- 감정 일기 포토북 생성 기능
- 커뮤니티/공감 기능 확장

---

## 📂 프로젝트 구조 일부

```bash
farstar/
├── users/ # 인증, 프로필 관리
├── stars/ # 별 정보 관리
├── posts/ # 감정 글 관리
├── constellations/ # 별자리 (예정)
├── lumen/ # 화폐 시스템 (예정)
├── payments/ # Stripe 결제 연동 (예정)
├── utils/ # 공통 유틸리티 (Skyfield 포함)
```