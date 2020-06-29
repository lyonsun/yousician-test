from tests.BaseTestCase import BaseTestCase


class TestHello(BaseTestCase):

    """
    test get endpoint to root route
    """

    def testHello(self):
        # request
        response = self.app.get(
            "/", headers={"Content-Type": "application/json"})

        # result
        self.assertEqual(response.data, b'{"Hello": "world"}')
        self.assertEqual(response.status_code, 200)
