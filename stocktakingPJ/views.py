import pandas as pd
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PostOffice

@api_view(['POST'])
def process_excel(request):
    try:
        raw_data = request.data.get('data', [])
        if not raw_data:
            return Response({"error": "Không có dữ liệu để xử lý."}, status=status.HTTP_400_BAD_REQUEST)
        df_input = pd.DataFrame(raw_data)

        if "Mã bưu cục" in df_input.columns:
            # 1. Lấy danh sách các mã bưu cục có note = "BC KH" từ DB (dưới dạng set các chuỗi)
            valid_post_offices = set(
                PostOffice.objects.filter(note="BC KH")
                .values_list('ma_buu_cuc', flat=True)
            )
            print(f"--> [3. Kết quả lọc] Số dòng còn lại: {len(valid_post_offices)}")
            valid_codes_str = {str(code).strip() for code in valid_post_offices if code is not None}

            # 2. Chuẩn hóa cột mã bưu cục của input về dạng chuỗi không có khoảng trắng thừa
            cleaned_codes = df_input['Mã bưu cục'].astype(str).str.strip()

            # 3. Lọc giữ lại các dòng thuộc danh sách mã hợp lệ (giữ nguyên các cột ban đầu)
            df_result = df_input[cleaned_codes.isin(valid_codes_str)].copy()
        else:
            df_result = df_input

        # Trả về dữ liệu chỉ chứa các cột gốc ban đầu
        return Response(df_result.to_dict(orient='records'))

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": f"Lỗi xử lý dữ liệu: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)