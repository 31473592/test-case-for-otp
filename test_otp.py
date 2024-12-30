import random
import string
import unittest
import time

class OTPSystem:
    def __init__(self, expiry_time=60):
        """
        Initialize the OTP system with an expiry time in seconds.
        """
        self.otp_store = {}
        self.expiry_time = expiry_time

    def generate_otp(self, user_id, length=6):
        """
        Generate a numeric OTP of a specified length for a user.
        """
        otp = ''.join(random.choices(string.digits, k=length))
        self.otp_store[user_id] = {"otp": otp, "timestamp": time.time()}
        return otp

    def validate_otp(self, user_id, otp):
        """
        Validate the OTP for a user.
        """
        if user_id not in self.otp_store:
            return False, "No OTP generated for this user."

        stored_otp_data = self.otp_store[user_id]
        if time.time() - stored_otp_data["timestamp"] > self.expiry_time:
            return False, "OTP expired."

        if stored_otp_data["otp"] == otp:
            return True, "OTP validated successfully."
        else:
            return False, "Invalid OTP."

class TestOTPSystem(unittest.TestCase):
    def setUp(self):
        """
        Set up the OTP system for testing.
        """
        self.otp_system = OTPSystem(expiry_time=5)

    def test_generate_otp(self):
        """
        Test OTP generation.
        """
        user_id = "user123"
        otp = self.otp_system.generate_otp(user_id)
        self.assertTrue(otp.isdigit())
        self.assertEqual(len(otp), 6)

    def test_validate_correct_otp(self):
        """
        Test OTP validation with the correct OTP.
        """
        user_id = "user123"
        otp = self.otp_system.generate_otp(user_id)
        is_valid, message = self.otp_system.validate_otp(user_id, otp)
        self.assertTrue(is_valid)
        self.assertEqual(message, "OTP validated successfully.")

    def test_validate_expired_otp(self):
        """
        Test OTP validation with an expired OTP.
        """
        user_id = "user123"
        otp = self.otp_system.generate_otp(user_id)
        time.sleep(6)  # Wait for OTP to expire
        is_valid, message = self.otp_system.validate_otp(user_id, otp)
        self.assertFalse(is_valid)
        self.assertEqual(message, "OTP expired.")

    def test_validate_invalid_otp(self):
        """
        Test OTP validation with an invalid OTP.
        """
        user_id = "user123"
        self.otp_system.generate_otp(user_id)
        is_valid, message = self.otp_system.validate_otp(user_id, "123456")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Invalid OTP.")

if __name__ == "__main__":
    unittest.main()
