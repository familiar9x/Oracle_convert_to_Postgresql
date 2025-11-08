# Quick Start Guide

## Bước 1: Cập nhật thông tin database trong file .env

```bash
nano .env
```

Cần điền đầy đủ:
- PostgreSQL: username, password, database name
- Oracle: username, password, service_name

## Bước 2: Activate virtual environment

```bash
source venv/bin/activate
```

## Bước 3: Test kết nối database

```bash
cd src
python db_connector.py
```

## Bước 4: Chạy chương trình chính

```bash
python main.py
```

Chọn các option:
- **Option 1**: Test kết nối cả 2 database
- **Option 2**: Extract và convert TẤT CẢ procedures/functions
- **Option 3**: Extract và convert theo schema cụ thể (khuyến nghị)
- **Option 4**: Convert một file SQL riêng lẻ
- **Option 5**: Test procedure đã convert trên PostgreSQL

## Workflow khuyến nghị

### 1. Extract procedures từ Oracle
```bash
python main.py
# Chọn option 3
# Nhập schema owner (ví dụ: HR, SALES, etc.)
# Nhập output directory (ví dụ: output/hr_schema)
```

### 2. Review code đã convert
```bash
ls -la output/hr_schema/
# Xem file *_oracle.sql (gốc)
# Xem file *_postgresql.sql (đã convert)
# Xem file *_conversion.log (log)
```

### 3. Manual review và chỉnh sửa (nếu cần)
```bash
nano output/hr_schema/MY_PROCEDURE_postgresql.sql
```

### 4. Test trên PostgreSQL
```bash
python main.py
# Chọn option 5
# Nhập path: output/hr_schema/MY_PROCEDURE_postgresql.sql
# Nhập test parameters (nếu có)
```

### 5. Deploy lên production (sau khi test OK)
```bash
psql -h 10.50.122.55 -p 5432 -U your_user -d your_db -f output/hr_schema/MY_PROCEDURE_postgresql.sql
```

## Các lệnh hữu ích

### Activate environment
```bash
source venv/bin/activate
```

### Deactivate environment
```bash
deactivate
```

### Run tests
```bash
pytest tests/test_converter.py -v
```

### Check database connections
```bash
# PostgreSQL
psql -h 10.50.122.55 -p 5432 -U your_user -d your_db

# Oracle
sqlplus your_user@//10.50.122.51:1521/your_service
```

## Troubleshooting

### cx_Oracle error: DPI-1047: Cannot locate Oracle Client library
Cần cài đặt Oracle Instant Client:

1. Download từ: https://www.oracle.com/database/technologies/instant-client/downloads.html
2. Giải nén vào thư mục (ví dụ: /opt/oracle/instantclient_21_1)
3. Set environment variable:
```bash
export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_1:$LD_LIBRARY_PATH
```

Hoặc thêm vào ~/.bashrc:
```bash
echo 'export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_1:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

### psycopg2 connection error
Kiểm tra:
- PostgreSQL service đang chạy: `sudo systemctl status postgresql`
- Firewall cho phép kết nối từ IP của bạn
- File pg_hba.conf cho phép kết nối từ host của bạn

## Tips

1. **Luôn test kết nối trước** (option 1)
2. **Extract theo schema** thay vì extract tất cả
3. **Review manual** trước khi deploy
4. **Backup** database trước khi chạy converted code
5. **Test với data thật** trước khi deploy production
