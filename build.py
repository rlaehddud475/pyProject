import subprocess
import sys


def build_exe():
  print("PyInstaller로 실행 파일 빌드를 시작합니다...")
  try:
    # 파이썬 내부에서 PyInstaller 모듈 호출
    subprocess.check_call(
        [sys.executable, "-m", "PyInstaller", "--noconsole", "--onefile", "main.py"]
    )
    print(
        "\n[성공] 빌드가 완료되었습니다! 폴더 내의 'dist' 폴더를 확인하세요."
    )
  except Exception as e:
    print(f"\n[오류 발생]: {e}")


if __name__ == "__main__":
  build_exe()
  input("\n종료하려면 엔터 키를 누르세요...")