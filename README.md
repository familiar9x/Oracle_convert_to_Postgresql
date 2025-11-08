# Oracle to PostgreSQL Conversion Tool

Tool chuyển đổi Functions/Procedures từ Oracle sang PostgreSQL và kiểm tra tính tương thích.

## Cấu hình Database

### PostgreSQL
- **Host**: 10.50.122.55
- **Port**: 5432

### Oracle
- **Host**: 10.50.122.51
- **Port**: 1521

## Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd Oracle_convert_to_Postgresql
```

### 2. Tạo Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment variables
```bash
cp .env.example .env
# Chỉnh sửa file .env với thông tin database của bạn
nano .env
```

Cần điền đầy đủ thông tin trong file `.env`:
```env
# PostgreSQL Configuration
PG_HOST=10.50.122.55
PG_PORT=5432
PG_DATABASE=your_database_name
PG_USER=your_username
PG_PASSWORD=your_password

# Oracle Configuration
ORACLE_HOST=10.50.122.51
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=your_service_name
ORACLE_USER=your_username
ORACLE_PASSWORD=your_password
```

## Cấu trúc Project

```
Oracle_convert_to_Postgresql/
├── src/
│   ├── db_connector.py      # Kết nối database
│   ├── converter.py          # Logic chuyển đổi Oracle -> PostgreSQL
│   └── main.py               # Script chính
├── tests/
│   └── test_converter.py     # Unit tests
├── output/                   # Thư mục chứa kết quả convert
├── requirements.txt          # Python dependencies
├── .env.example              # Mẫu cấu hình
├── .env                      # Cấu hình thực tế (không commit)
└── README.md
```

## Sử dụng

### Chạy script chính (Interactive Mode)
```bash
cd src
python main.py
```

Menu tương tác sẽ hiện ra với các tùy chọn:
1. Test kết nối database
2. Extract và convert tất cả procedures/functions
3. Extract và convert theo schema owner
4. Convert một file SQL đơn lẻ
5. Test procedure đã convert trên PostgreSQL
0. Thoát

### Test kết nối database
```bash
cd src
python db_connector.py
```

### Chạy tests
```bash
pytest tests/test_converter.py -v
```

## Quy trình Conversion

### 1. Extract từ Oracle
Script sẽ:
- Kết nối đến Oracle database
- Lấy danh sách tất cả procedures/functions
- Đọc source code của từng object
- Lưu file Oracle gốc (`*_oracle.sql`)

### 2. Convert sang PostgreSQL
Converter sẽ tự động chuyển đổi:
- ✅ `CREATE PROCEDURE` → `CREATE FUNCTION`
- ✅ Data types: `NUMBER` → `NUMERIC`, `VARCHAR2` → `VARCHAR`, etc.
- ✅ `SYSDATE` → `CURRENT_TIMESTAMP`
- ✅ `NVL()` → `COALESCE()`
- ✅ Sequences: `seq.NEXTVAL` → `NEXTVAL('seq')`
- ✅ `FROM DUAL` → removed
- ✅ `ROWNUM` → `LIMIT`
- ✅ Exception handling
- ✅ Cursor syntax

### 3. Test trên PostgreSQL
- Load converted function vào PostgreSQL
- Test với dữ liệu mẫu
- Verify kết quả

## Output Files

Sau khi chạy conversion, trong thư mục `output/` sẽ có:
- `<procedure_name>_oracle.sql` - Code Oracle gốc
- `<procedure_name>_postgresql.sql` - Code PostgreSQL đã convert
- `<procedure_name>_conversion.log` - Log quá trình conversion

## Ví dụ sử dụng

### Convert một procedure cụ thể
```python
from converter import convert_file

convert_file(
    'input/my_procedure_oracle.sql',
    'output/my_procedure_postgresql.sql'
)
```

### Extract tất cả procedures từ một schema
```python
from main import extract_and_convert

extract_and_convert(owner='MY_SCHEMA', output_dir='output/my_schema')
```

### Test procedure đã convert
```python
from main import test_converted_procedure

test_converted_procedure(
    'output/my_procedure_postgresql.sql',
    test_data="'param1', 123"
)
```

## Lưu ý quan trọng

1. **Manual Review**: Luôn review code đã convert trước khi sử dụng production
2. **Complex Logic**: Một số logic phức tạp có thể cần chỉnh sửa thủ công
3. **Performance**: Test performance của converted functions
4. **Data Types**: Kiểm tra kỹ data types, đặc biệt với NUMBER và DATE
5. **Dependencies**: Đảm bảo tất cả dependencies (tables, sequences, etc.) đã được migrate

## Các conversion cần review thủ công

- `NVL2()` - Phức tạp hơn `NVL()`
- `DECODE()` - Cần convert thành `CASE WHEN`
- `CONNECT BY` - Hierarchical queries
- `ROWNUM` trong complex queries
- Package dependencies
- Triggers
- Custom types

## Troubleshooting

### Lỗi kết nối Oracle
```bash
# Kiểm tra Oracle Instant Client đã được cài đặt
# Download từ: https://www.oracle.com/database/technologies/instant-client/downloads.html
```

### Lỗi kết nối PostgreSQL
```bash
# Kiểm tra pg_hba.conf cho phép kết nối từ IP của bạn
# Kiểm tra PostgreSQL service đang chạy
```

## Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:
1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push và tạo Pull Request

## License

MIT License
