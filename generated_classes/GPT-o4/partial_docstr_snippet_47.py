class API:
    def __init__(self, user, repo, token=None, password=None):
        '''
        param user: str -> Github username
        param token: str -> Github oauth token
        param repo: str -> Github repository name
        param password: str -> Github user password
        '''
        self.user = user
        self.repo = repo
        if token:
            self.auth = (user, token)
        elif password:
            self.auth = (user, password)
        else:
            raise ValueError("Either token or password must be provided")

    def create_comment_commit(self, body, commit_id, path, position, pr_id):
        '''
        Posts a comment to a given commit at a certain pull request.
        Check https://developer.github.com/v3/pulls/comments/#create-a-comment

        param body: str -> Comment text
        param commit_id: str -> SHA of the commit
        param path: str -> Relative path of the file to be commented
        param position: int -> The position in the diff to add a review comment
        param pr_id: int -> Github pull request id
        '''
        url = f"https://api.github.com/repos/{self.user}/{self.repo}/pulls/{pr_id}/comments"
        payload = {
            "body": body,
            "commit_id": commit_id,
            "path": path,
            "position": position
        }
        response = requests.post(url, json=payload, auth=self.auth)
        response.raise_for_status()
        return response.json()