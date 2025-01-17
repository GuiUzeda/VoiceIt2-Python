from voiceit2 import VoiceIt2
import os
import unittest
import urllib

users_to_delete = []
groups_to_delete = []
VI_KEY = os.environ['VIAPIKEY']
VI_TOKEN = os.environ['VIAPITOKEN']
VOICEIT_DRIVE_URL = 'https://drive.voiceit.io/files/'
PHRASE = 'never forget tomorrow is a new day'
CONTENT_LANGUAGE = 'en-US'

def downloadS3File(fileName):
    urllib.request.urlretrieve(VOICEIT_DRIVE_URL + fileName, fileName)

class TestVoiceIt2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Started Downloading Test Files ...')
        downloadS3File('enrollmentBMyFaceAndVoice.m4a')
        downloadS3File('enrollmentA1.wav')
        downloadS3File('enrollmentA2.wav')
        downloadS3File('enrollmentA3.wav')
        downloadS3File('verificationA1.wav')
        downloadS3File('enrollmentC1.wav')
        downloadS3File('enrollmentC2.wav')
        downloadS3File('enrollmentC3.wav')
        downloadS3File('videoEnrollmentB1.mov')
        downloadS3File('videoEnrollmentB2.mov')
        downloadS3File('videoEnrollmentB3.mov')
        downloadS3File('videoVerificationB1.mov')
        downloadS3File('videoEnrollmentC1.mov')
        downloadS3File('videoEnrollmentC2.mov')
        downloadS3File('videoEnrollmentC3.mov')
        downloadS3File('faceEnrollmentB1.mp4')
        downloadS3File('faceEnrollmentB2.mp4')
        downloadS3File('faceEnrollmentB3.mp4')
        downloadS3File('faceVerificationB1.mp4')
        downloadS3File('faceVerificationC1.mp4')
        downloadS3File('faceEnrollmentA1.mov')
        downloadS3File('faceEnrollmentA2.mov')
        downloadS3File('faceEnrollmentA3.mov')
        downloadS3File('videoEnrollmentA1.mov')
        downloadS3File('videoEnrollmentA2.mov')
        downloadS3File('videoEnrollmentA3.mov')
        print('Done Downloading Test Files')

    # Method called once at the end of all tests
    @classmethod
    def tearDownClass(cls):
        global groups_to_delete,users_to_delete
        my_voiceit = VoiceIt2(VI_KEY, VI_TOKEN)
        for user_id in users_to_delete:
            my_voiceit.delete_user(user_id)
        for group_id in groups_to_delete:
            my_voiceit.delete_group(group_id)

    # Check if api key and token can be found in the environment variables
    def test_webhooks(self):
        print('Testing Notification URL')
        my_voiceit = VoiceIt2(VI_KEY, VI_TOKEN)
        if os.environ['BOXFUSE_ENV'] == 'voiceittest':
            text_file = open(os.environ['HOME'] + '/platformVersion', "w")
            text_file.write(my_voiceit.version)
            text_file.close()
        my_voiceit.add_notification_url('https://voiceit.io')
        self.assertEqual(my_voiceit.notification_url, '?notificationURL=https%3A%2F%2Fvoiceit.io')
        my_voiceit.remove_notification_url()
        self.assertEqual(my_voiceit.notification_url, '')


    # Check if api key and token can be found in the environment variables
    def test_api_key_token(self):
        print('Testing Key/Token Environment Variables')
        self.assertNotEqual(VI_KEY, '')
        self.assertNotEqual(VI_TOKEN, '')

    def test_file_not_found(self):
        my_voiceit = VoiceIt2(VI_KEY, VI_TOKEN)
        print('Testing File Not Found')
        print('   Testing File Not Found Enrollment')
        try:
            my_voiceit.create_voice_enrollment('', CONTENT_LANGUAGE, PHRASE, './nonexistent.wav')
            self.assertTrue(False)
        except IOError:
            self.assertTrue(True)

        try:
            my_voiceit.create_face_enrollment('', './nonexistent.mov')
            self.assertTrue(False)
        except IOError:
            self.assertTrue(True)

        try:
            my_voiceit.create_video_enrollment('', CONTENT_LANGUAGE, PHRASE, './nonexistent.mov')
            self.assertTrue(False)
        except IOError:
            self.assertTrue(True)

        print('   Testing File Not Found Verification')
        try:
            my_voiceit.voice_verification('', CONTENT_LANGUAGE, PHRASE, './nonexistent.wav')
            self.assertTrue(False)
        except IOError:
            self.assertTrue(True)

        try:
            my_voiceit.face_verification('', './nonexistent.mov')
            self.assertTrue(False)
        except IOError:
            self.assertTrue(True)

        try:
            my_voiceit.video_verification('', CONTENT_LANGUAGE, PHRASE, './nonexistent.mov')
            self.assertTrue(False)
        except IOError:
            self.assertTrue(True)

        print('   Testing File Not Found Identification')
        try:
            my_voiceit.voice_identification('', CONTENT_LANGUAGE, PHRASE, './nonexistent.wav')
            self.assertTrue(False)
        except IOError:
            self.assertTrue(True)

        try:
            my_voiceit.face_identification('', './nonexistent.mov')
            self.assertTrue(False)
        except IOError:
            self.assertTrue(True)

        try:
            my_voiceit.video_identification('', CONTENT_LANGUAGE, PHRASE, './nonexistent.mov')
            self.assertTrue(False)
        except IOError:
            self.assertTrue(True)

    def test_users(self):
        my_voiceit = VoiceIt2(VI_KEY, VI_TOKEN)
        global users_to_delete
        print('Testing User API Calls')

        print('   Testing Get All Users')
        ret = my_voiceit.get_all_users()
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertGreaterEqual(len(ret['users']), 0)

        print('   Testing Create User')
        ret = my_voiceit.create_user()
        self.assertEqual(201, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        user_id = ret['userId']
        users_to_delete.append(user_id)

        print('   Testing Check User Exists')
        ret = my_voiceit.check_user_exists(user_id)
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Testing Get Groups For User')
        ret = my_voiceit.get_groups_for_user(user_id)
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(0, len(my_voiceit.get_groups_for_user(user_id)['groups']))

        print('   Testing Create User Token')
        ret = my_voiceit.create_user_token(user_id, 5)
        self.assertEqual(201, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Testing Expire User Tokens')
        ret = my_voiceit.expire_user_tokens(user_id)
        self.assertEqual(201, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Testing Delete User')
        ret = my_voiceit.delete_user(user_id)
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

    def test_phrases(self):
        my_voiceit = VoiceIt2(VI_KEY, VI_TOKEN)
        print('Testing Phrase API Calls')

        print('   Testing Get Phrases')
        ret = my_voiceit.get_phrases('en-US')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertGreaterEqual(len(ret['phrases']), 0)

    def test_groups(self):
        my_voiceit = VoiceIt2(VI_KEY, VI_TOKEN)
        global groups_to_delete,users_to_delete
        print('Test Group API Calls')

        print('   Test Create Group')
        ret = my_voiceit.create_group('Sample Group Description')
        self.assertEqual(201, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        group_id = ret['groupId']
        groups_to_delete.append(group_id)

        print('   Test Get Group')
        ret = my_voiceit.get_group(group_id)
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Test Get All Groups')
        ret = my_voiceit.get_all_groups()
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertGreaterEqual(len(ret['groups']), 0)

        print('   Test Group Exists')
        ret = my_voiceit.group_exists(group_id)
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(True, ret['exists'])

        user_id = my_voiceit.create_user()['userId']
        users_to_delete.append(user_id)

        print('   Test Add User to Group')
        ret = my_voiceit.add_user_to_group(group_id, user_id)
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Test Remove User from Group')
        ret = my_voiceit.remove_user_from_group(group_id, user_id)
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Test Delete Group')
        ret = my_voiceit.delete_group(group_id)
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

    def test_enrollments(self):
        my_voiceit = VoiceIt2(VI_KEY, VI_TOKEN)
        ret = my_voiceit.create_user()
        user_id = my_voiceit.create_user()['userId']
        users_to_delete.append(user_id)
        print('Test Enrollment API Calls')

        print('   Test Get All Face Enrollments')
        ret = my_voiceit.get_all_face_enrollments(user_id)
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertGreaterEqual(len(ret['faceEnrollments']), 0)

        print('   Test Get All Voice Enrollments')
        ret = my_voiceit.get_all_voice_enrollments(user_id)
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertGreaterEqual(len(ret['voiceEnrollments']), 0)

        print('   Test Get All Video Enrollments')
        ret = my_voiceit.get_all_video_enrollments(user_id)
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertGreaterEqual(len(ret['videoEnrollments']), 0)

        print('   Test Create Voice Enrollment')
        ret = my_voiceit.create_voice_enrollment(user_id, CONTENT_LANGUAGE, PHRASE, './enrollmentA1.wav')
        self.assertEqual(201, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        enrollment_id_to_delete = ret['id']

        print('   Test Create Voice Enrollment by URL')
        ret = my_voiceit.create_voice_enrollment_by_url(user_id, CONTENT_LANGUAGE, PHRASE, VOICEIT_DRIVE_URL + 'enrollmentA2.wav')
        self.assertEqual(201, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Test Create Face Enrollment')
        ret = my_voiceit.create_face_enrollment(user_id, './faceEnrollmentA1.mov')
        self.assertEqual(201, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        enrollment_id_to_delete = ret['faceEnrollmentId']

        print('   Test Create Face Enrollment by URL')
        ret = my_voiceit.create_face_enrollment_by_url(user_id, VOICEIT_DRIVE_URL + 'faceEnrollmentA2.mov')
        self.assertEqual(201, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Test Create Video Enrollment')
        ret = my_voiceit.create_video_enrollment(user_id, CONTENT_LANGUAGE, PHRASE, './videoEnrollmentA1.mov')
        self.assertEqual(201, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        enrollment_id_to_delete = ret['id']

        print('   Test Create Video Enrollment by URL')
        ret = my_voiceit.create_video_enrollment_by_url(user_id, CONTENT_LANGUAGE, PHRASE, VOICEIT_DRIVE_URL + 'videoEnrollmentA2.mov')
        self.assertEqual(201, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Test Delete All Enrollments')
        ret = my_voiceit.delete_all_enrollments(user_id)
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

    def test_verification(self):
        my_voiceit = VoiceIt2(VI_KEY, VI_TOKEN)
        user_id = my_voiceit.create_user()['userId']
        users_to_delete.append(user_id)
        # Create 3 voice,face and video enrollments for user
        my_voiceit.create_voice_enrollment(user_id, CONTENT_LANGUAGE, PHRASE, './enrollmentA1.wav')
        my_voiceit.create_voice_enrollment(user_id, CONTENT_LANGUAGE, PHRASE, './enrollmentA2.wav')
        my_voiceit.create_voice_enrollment(user_id, CONTENT_LANGUAGE, PHRASE, './enrollmentA3.wav')
        my_voiceit.create_face_enrollment(user_id, './faceEnrollmentB1.mp4')
        my_voiceit.create_face_enrollment(user_id, './faceEnrollmentB2.mp4')
        my_voiceit.create_face_enrollment(user_id, './faceEnrollmentB3.mp4')
        my_voiceit.create_video_enrollment(user_id, CONTENT_LANGUAGE, PHRASE, './videoEnrollmentB1.mov')
        my_voiceit.create_video_enrollment(user_id, CONTENT_LANGUAGE, PHRASE, './videoEnrollmentB2.mov')
        my_voiceit.create_video_enrollment(user_id, CONTENT_LANGUAGE, PHRASE, './videoEnrollmentB3.mov')

        print('Test Verification API Calls')

        print('   Test Voice Verification')
        ret = my_voiceit.voice_verification(user_id, CONTENT_LANGUAGE, PHRASE, './verificationA1.wav')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Test Voice Verification by URL')
        ret = my_voiceit.voice_verification_by_url(user_id, CONTENT_LANGUAGE, PHRASE, VOICEIT_DRIVE_URL + 'enrollmentA4.wav')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Test Face Verification')
        ret = my_voiceit.face_verification(user_id, './faceVerificationB1.mp4')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Test Face Verification by URL')
        ret = my_voiceit.face_verification_by_url(user_id, VOICEIT_DRIVE_URL + 'faceVerificationB1.mp4')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Test Video Verification')
        ret = my_voiceit.video_verification(user_id, CONTENT_LANGUAGE, PHRASE, './videoVerificationB1.mov')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

        print('   Test Video Verification by URL')
        ret = my_voiceit.video_verification_by_url(user_id, CONTENT_LANGUAGE, PHRASE, VOICEIT_DRIVE_URL + 'videoVerificationB2.mp4')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])

    def test_identification(self):
        my_voiceit = VoiceIt2(VI_KEY, VI_TOKEN)
        global groups_to_delete,users_to_delete
        print('Start Identification Setup...')
        user_id_1 = my_voiceit.create_user()['userId']
        users_to_delete.append(user_id_1)
        user_id_2 = my_voiceit.create_user()['userId']
        users_to_delete.append(user_id_2)
        group_id = my_voiceit.create_group('Test Identification Group')['groupId']
        groups_to_delete.append(group_id)
        my_voiceit.add_user_to_group(group_id, user_id_1)
        my_voiceit.add_user_to_group(group_id, user_id_2)

        # Create 3 voice enrollments for each user
        for file in ['./enrollmentA1.wav','./enrollmentA2.wav','./enrollmentA3.wav']:
            my_voiceit.create_voice_enrollment(user_id_1, CONTENT_LANGUAGE, PHRASE, file)
        for file in ['./enrollmentC1.wav','./enrollmentC2.wav','./enrollmentC3.wav']:
            my_voiceit.create_voice_enrollment(user_id_2, CONTENT_LANGUAGE, PHRASE, file)
        # Create 3 video enrollments for each user
        for file in ['./videoEnrollmentB1.mov','./videoEnrollmentB2.mov','./videoEnrollmentB3.mov']:
            my_voiceit.create_video_enrollment(user_id_1, CONTENT_LANGUAGE, PHRASE, file)
        for file in ['./videoEnrollmentC1.mov','./videoEnrollmentC2.mov','./videoEnrollmentC3.mov']:
            my_voiceit.create_video_enrollment(user_id_2, CONTENT_LANGUAGE, PHRASE, file)

        print('Test Identification API Calls')

        print('   Test Voice Identification')
        ret = my_voiceit.voice_identification(group_id, CONTENT_LANGUAGE, PHRASE, './enrollmentA1.wav')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(user_id_1, ret['userId'])
        ret = my_voiceit.voice_identification(group_id, CONTENT_LANGUAGE, PHRASE, './enrollmentC1.wav')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(user_id_2, ret['userId'])

        print('   Test Voice Identification by URL')
        ret = my_voiceit.voice_identification_by_url(group_id, CONTENT_LANGUAGE, PHRASE, VOICEIT_DRIVE_URL + 'enrollmentA1.wav')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(user_id_1, ret['userId'])
        ret = my_voiceit.voice_identification_by_url(group_id, CONTENT_LANGUAGE, PHRASE, VOICEIT_DRIVE_URL + 'enrollmentC1.wav')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(user_id_2, ret['userId'])

        print('   Test Face Identification')
        ret = my_voiceit.face_identification(group_id, './faceVerificationB1.mp4')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(user_id_1, ret['userId'])
        ret = my_voiceit.face_identification(group_id, './faceVerificationC1.mp4')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(user_id_2, ret['userId'])

        print('   Test Face Identification by URL')
        ret = my_voiceit.face_identification_by_url(group_id, VOICEIT_DRIVE_URL + 'faceVerificationB1.mp4')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(user_id_1, ret['userId'])
        ret = my_voiceit.face_identification_by_url(group_id, VOICEIT_DRIVE_URL + 'faceVerificationC1.mp4')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(user_id_2, ret['userId'])

        print('   Test Video Identification')
        ret = my_voiceit.video_identification(group_id, CONTENT_LANGUAGE, PHRASE, './videoEnrollmentB1.mov')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(user_id_1, ret['userId'])
        ret = my_voiceit.video_identification(group_id, CONTENT_LANGUAGE, PHRASE, './videoEnrollmentC1.mov')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(user_id_2, ret['userId'])

        print('   Test Video Identification by URL')
        ret = my_voiceit.video_identification_by_url(group_id, CONTENT_LANGUAGE, PHRASE, VOICEIT_DRIVE_URL + 'videoEnrollmentB1.mov')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(user_id_1, ret['userId'])
        ret = my_voiceit.video_identification_by_url(group_id, CONTENT_LANGUAGE, PHRASE, VOICEIT_DRIVE_URL + 'videoEnrollmentC1.mov')
        self.assertEqual(200, ret['status'])
        self.assertEqual('SUCC', ret['responseCode'])
        self.assertEqual(user_id_2, ret['userId'])

if __name__ == '__main__':
    unittest.main()
