## 사용자

### 회원 가입

#### 요청

```
POST {{API_URL}}/api/v1/accounts/signup/
```

| 파라미터    | 파라미터 유형 | 데이터 타입 | 필수 여부 | 설명          |
| ----------- | ------------- | ----------- | --------- | ------------- |
| `email`     | `body`        | `string`    | required  | 이메일        |
| `password1` | `body`        | `string`    | required  | 비밀번호      |
| `password2` | `body`        | `string`    | required  | 비밀번호 확인 |

#### 응답

| 키        | 데이터 타입 | 설명           |
| --------- | ----------- | -------------- |
| `message` | `string`    | 성공시 success |
| `email`   | `string`    | 유저의 email   |
| `token`   | `string`    | 인증 토큰      |

```json5
{
  "message": "success",
  "email": "YOUR EMAIL",
  "token": "YOUR ACCESS TOKEN"
}
```

### 로그인

#### 요청

```
POST {{API_URL}}/api/v1/accounts/login/
```

| 파라미터   | 파라미터 유형 | 데이터 타입 | 필수 여부 | 설명     |
| ---------- | ------------- | ----------- | --------- | -------- |
| `email`    | `body`        | `string`    | required  | 이메일   |
| `password` | `body`        | `string`    | required  | 비밀번호 |

#### 응답

| 키        | 데이터 타입 | 설명           |
| --------- | ----------- | -------------- |
| `message` | `string`    | 성공시 success |
| `token`   | `string`    | 인증 토큰      |

```json5
{
  "message": "success",
  "token": "YOUR ACCESS TOKEN"
}
```

## 책

### 책 목록

#### 요청

```
GET {{API_URL}}/api/v1/books/?ordering={ordering}&page={page}
```

| 파라미터   | 파라미터 유형 | 데이터 타입 | 필수 여부                    | 설명        |
| ---------- | ------------- | ----------- | ---------------------------- | ----------- |
| `ordering` | `query`       | `string`    | optional, (기본값) -avg_star | 정렬        |
| `page`     | `query`       | `string`    | optional, (기본값) 1         | 페이지 번호 |

#### 응답

| 키         | 데이터 타입            | 설명              |
| ---------- | ---------------------- | ----------------- |
| `count`    | `number`               | 책의 총 권수      |
| `next`     | `URL`                  | 다음 페이지의 URL |
| `previous` | `URL`                  | 이전 페이지의 URL |
| `results`  | `array of Book object` | 결과              |

```json5
{
  "count": 143,
  "next": "http://127.0.0.1:8000/api/v1/books/?page=2",
  "previous": null,
  "results": [
    {
      "title": "TITLE",
      "author": "AUTHOR",
      "publisher": "PUBLISHER",
      "pub_year": "PUB_YEAR",
      "isbn": "ISBN, unique key",
      "description": "DESCRIPTION",
      "bookImage": "BOOKIMAGE",
      "review": [
        ...
      ]
      "keywords": [
        ...
      ],
      "num_views": 8,
      "like_count": 1,
      "review_count": 4,
      "avg_star": 5
    },
    {
    ...

    }
}
```

### 책 검색

#### 요청

```
GET {{API_URL}}/api/v1/books/?search={search}&ordering={ordering}&page={page}
```

| 파라미터   | 파라미터 유형 | 데이터 타입 | 필수 여부                    | 설명        |
| ---------- | ------------- | ----------- | ---------------------------- | ----------- |
| `search`   | `query`       | `string`    | required                     | 검색        |
| `ordering` | `query`       | `string`    | optional, (기본값) -avg_star | 정렬        |
| `page`     | `query`       | `string`    | optional, (기본값) 1         | 페이지 번호 |

#### 응답

| 키         | 데이터 타입            | 설명              |
| ---------- | ---------------------- | ----------------- |
| `count`    | `number`               | 책의 총 권수      |
| `next`     | `URL`                  | 다음 페이지의 URL |
| `previous` | `URL`                  | 이전 페이지의 URL |
| `results`  | `array` | 결과              |

```json5
{
  "count": 143,
  "next": "http://127.0.0.1:8000/api/v1/books/?page=2",
  "previous": null,
  "results": [
    {
      "title": "TITLE",
      "author": "AUTHOR",
      "publisher": "PUBLISHER",
      "pub_year": "PUB_YEAR",
      "isbn": "ISBN, unique key",
      "description": "DESCRIPTION",
      "bookImage": "BOOKIMAGE",
      "review": [
        ...
      ],
      "keywords": [
        ...
      ],
      "num_views": 8,
      "like_count": 1,
      "review_count": 4,
      "avg_star": 5
    },
    {
    ...

    }
}
```

### 책 생성

#### 요청

```
POST {{API_URL}}/api/v1/books/
```

| 파라미터 | 파라미터 유형 | 데이터 타입 | 필수 여부 | 설명                             |
| -------- | ------------- | ----------- | --------- | -------------------------------- |
| `isbn`   | `body`        | `string`    | required  | 13자리 숫자로 이루어진 ISBN 번호 |

#### 응답

| 키             | 데이터 타입 | 설명                     |
| -------------- | ----------- | ------------------------ |
| `title`        | `string`    | 책 제목                  |
| `author`       | `string`    | 저자                     |
| `publisher`    | `string`    | 출판사                   |
| `pub_year`     | `string`    | 출판년도                 |
| `isbn`         | `string`    | 13자리 ISBN              |
| `description`  | `string`    | 책의 요약 내용           |
| `review`       | `array`     | 리뷰의 배열              |
| `keywords`     | `array`     | 관련 키워드의 배열       |
| `num_views`    | `number`    | 조회수                   |
| `like_count`   | `number`    | 구독(또는 좋아요)의 개수 |
| `review_count` | `number`    | 리뷰의 개수              |

```json5
{
  "title": "TITLE",
  "author": "AUTHOR",
  "publisher": "PUBLISHER",
  "pub_year": "PUB_YEAR",
  "isbn": "ISBN, unique key",
  "description": "DESCRIPTION",
  "bookImage": "BOOKIMAGE",
  "review": [],
  "keywords": [],
  "num_views": 0,
  "like_count": 0,
  "review_count": 0
}
```

### 책 상세 정보


#### 요청

```
GET {API_URL} /api/v1/books/{isbn}/
```

| 파라미터 | 파라미터 유형 | 데이터 타입 | 필수 여부 | 설명                             |
| -------- | ------------- | ----------- | --------- | -------------------------------- |
| `isbn`   | `path`        | `string`    | required  | 13자리 숫자로 이루어진 ISBN 번호 |

#### 응답

| 키             | 데이터 타입 | 설명                     |
| -------------- | ----------- | ------------------------ |
| `title`        | `string`    | 책 제목                  |
| `author`       | `string`    | 저자                     |
| `publisher`    | `string`    | 출판사                   |
| `pub_year`     | `string`    | 출판년도                 |
| `isbn`         | `string`    | 13자리 ISBN              |
| `description`  | `string`    | 책의 요약 내용           |
| `review`       | `array`     | 리뷰의 배열              |
| `keywords`     | `array`     | 관련 키워드의 배열       |
| `num_views`    | `number`    | 조회수                   |
| `like_count`   | `number`    | 구독(또는 좋아요)의 개수 |
| `review_count` | `number`    | 리뷰의 개수              |

```json5
{
  "title": "TITLE",
  "author": "AUTHOR",
  "publisher": "PUBLISHER",
  "pub_year": "PUB_YEAR",
  "isbn": "ISBN, unique key",
  "description": "DESCRIPTION",
  "bookImage": "BOOKIMAGE",
  "review": [],
  "keywords": [],
  "num_views": 0,
  "like_count": 0,
  "review_count": 0
}
```

### 책 연관 키워드


#### 요청

```
GET {API_URL} /api/v1/books/{isbn}/keywords/
```

| 파라미터 | 파라미터 유형 | 데이터 타입 | 필수 여부 | 설명                             |
| -------- | ------------- | ----------- | --------- | -------------------------------- |
| `isbn`   | `path`        | `string`    | required  | 13자리 숫자로 이루어진 ISBN 번호 |

#### 응답

| 키             | 데이터 타입 | 설명                     |
| -------------- | ----------- | ------------------------ |
| `word`        | `string`    | 키워드            |
| `weight`       | `string`    | 가중치                    |

```json5
[
	{
		"word": "WORD",
		"weight": "WEIGHT",
	},
	{
		...

	}
]
```

### 연관 도서 추천


#### 요청

```
GET {API_URL} /api/v1/books/{isbn}/recommend/
```

| 파라미터 | 파라미터 유형 | 데이터 타입 | 필수 여부 | 설명                             |
| -------- | ------------- | ----------- | --------- | -------------------------------- |
| `isbn`   | `path`        | `string`    | required  | 13자리 숫자로 이루어진 ISBN 번호 |

#### 응답

| 키             | 데이터 타입 | 설명                     |
| -------------- | ----------- | ------------------------ |
| `isbn`        | `string`    | 키워드            |
| `title`       | `string`    | 제목 |
| `author`       | `string`   | 저자 |
| `pub_year`       | `string`    | 출판년도 |

```json5
[
	{
		"isbn": "ISBN", 
		"title": "TITLE",
		"author": "AUTHOR",
		"pub_year": "PUB_YEAR""
	},
	{
		...

	}
]
```
