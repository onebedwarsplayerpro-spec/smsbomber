import sys
import subprocess
import importlib
import platform

class AutoInstaller:
    def __init__(self):
        self.system_info = {
            'os': platform.system(),
            'python_version': sys.version,
            'architecture': platform.architecture()[0]
        }
        
        self.libraries = {
            'essential': ['requests', 'colorama', 'threading', 'datetime', 'random', 'time', 'json'],
            'gui': ['tkinter', 'pyqt5', 'kivy'],
            'web': ['selenium', 'beautifulsoup4', 'scrapy', 'urllib3'],
            'data': ['pandas', 'numpy', 'matplotlib', 'openpyxl'],
            'advanced': ['pyautogui', 'opencv-python', 'pillow', 'pyinstaller']
        }
    
    def show_welcome(self):
        """نمایش صفحه خوش آمدگویی"""
        print("🐍 پایتون اتو اینستالر")
        print("=" * 50)
        print(f"سیستم عامل: {self.system_info['os']}")
        print(f"معماری: {self.system_info['architecture']}")
        print(f"پایتون: {self.system_info['python_version'].split()[0]}")
        print("=" * 50)
    
    def check_admin(self):
        """بررسی دسترسی ادمین"""
        try:
            if self.system_info['os'] == 'Windows':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except:
            return False
    
    def install_category(self, category_name, libraries):
        """نصب یک دسته از کتابخانه‌ها"""
        print(f"\n📁 نصب دسته {category_name}...")
        success_count = 0
        
        for lib in libraries:
            try:
                importlib.import_module(lib)
                print(f"   ✅ {lib} (از قبل نصب شده)")
                success_count += 1
            except ImportError:
                try:
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", lib, 
                        "--quiet", "--no-warn-script-location"
                    ])
                    print(f"   ✅ {lib} (نصب شد)")
                    success_count += 1
                except:
                    print(f"   ❌ {lib} (خطا در نصب)")
        
        return success_count, len(libraries)
    
    def run_installation(self):
        """اجرای فرآیند نصب"""
        self.show_welcome()
        
        # نمایش دسته‌ها
        print("\n📚 دسته‌های کتابخانه‌های قابل نصب:")
        for i, category in enumerate(self.libraries.keys(), 1):
            print(f"{i}. {category} ({len(self.libraries[category])} کتابخانه)")
        
        # انتخاب کاربر
        print("\n🎯 انتخاب دسته:")
        print("0. نصب همه کتابخانه‌ها")
        for i, category in enumerate(self.libraries.keys(), 1):
            print(f"{i}. فقط {category}")
        
        try:
            choice = int(input("\nلطفا عدد مورد نظر را وارد کنید: "))
        except:
            choice = 0
        
        # نصب بر اساس انتخاب
        total_success = 0
        total_libraries = 0
        
        if choice == 0:
            # نصب همه
            for category, libs in self.libraries.items():
                success, total = self.install_category(category, libs)
                total_success += success
                total_libraries += total
        else:
            # نصب دسته خاص
            categories = list(self.libraries.keys())
            if 1 <= choice <= len(categories):
                category = categories[choice-1]
                total_success, total_libraries = self.install_category(
                    category, self.libraries[category]
                )
        
        # نمایش نتیجه
        print("\n" + "=" * 50)
        print(f"📊 نتیجه نهایی:")
        print(f"✅ موفق: {total_success}")
        print(f"❌ ناموفق: {total_libraries - total_success}")
        print(f"📈 نرخ موفقیت: {(total_success/total_libraries)*100:.1f}%")
        
        if total_success == total_libraries:
            print("🎉 تمام کتابخانه‌ها با موفقیت نصب شدند!")
        else:
            print("⚠️  برخی کتابخانه‌ها نصب نشدند")

if __name__ == "__main__":
    installer = AutoInstaller()
    installer.run_installation()
