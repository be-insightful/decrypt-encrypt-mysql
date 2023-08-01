# de

암호 관리 페이지
encrypt <=> decrypt

## working directory
`de`

## run
```bash
docker-compose up -d
```

## docker-compose up 이후, 테이블 생성, 데이터 입력
### docker 접속
```bash
docker exec -it mysql /bin/bash
```

### 테이블 
- `authentication`: 암복호화 사용 master key 저장
- `user`: 로그인 사용자 관리