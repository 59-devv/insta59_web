from instaloader import *

# 인스타로더 생성
L = instaloader.Instaloader()


# 로그인
def login_action():
    login_id = ["YOUR_ID_HERE", "YOUR_ID_HERE_2", "YOUR_ID_HERE_3"]
    login_pw = "YOUR_PASSWORD_HERE"

    for i in range(len(login_id)):
        try:
            L.login(login_id[i], login_pw)
            break
        except:
            pass


# 1. 키워드가 있는지 포스팅마다 검색하는 함수
def keyword_check(prof: str, num: int, key: str):
    login_action()

    target_prof = prof
    search_num = num
    profile = Profile.from_username(L.context, target_prof)
    posts = profile.get_posts()

    keys = key
    key_count = 0
    analysis_list = []
    cnt = 0

    # 분석
    for i in posts:
        cnt += 1
        if keys in i.caption:
            analysis_list.append({"thumbnail": i.url, "url": i.shortcode, "caption": i.caption})
            key_count += 1
        if cnt == search_num:
            break

    return analysis_list


# 2. 단일 계정 분석하기
def test_single_account_check(prof: str):
    login_action()

    target_prof = prof
    profile = Profile.from_username(L.context, target_prof)
    posts = profile.get_posts()

    # 게시글 15개 분석 (단, 게시글이 15개 미만일 경우 게시글 수 만큼 분석)
    cnt = 0
    total_likes = 0
    total_comments = 0
    photos = []
    for i in posts:
        cnt += 1
        total_likes += i.likes
        total_comments += i.comments
        photos.append([i.url, f"https://www.instagram.com/p/{i.shortcode}"])
        if profile.mediacount > 15:
            if cnt == 15:
                break
        else:
            if cnt == profile.mediacount:
                break

    account = f"https://www.instagram.com/{prof}"
    followers = profile.followers
    avg_likes = total_likes / 15
    avg_comments = total_comments / 15

    result = {"account": account, "followers": format(followers, ","), "avg_likes": round(avg_likes, 2),
              "avg_comments": round(avg_comments, 2), "photos": photos}

    return result


# 3. 여러 계정 분석하는 함수
def multi_account_check(account):
    login_action()

    account_array = account

    # 계정명 오류가 나온 계정에 대한 변수
    error_account = 0
    error_account_list = []
    cnt = 0

    final = []
    # 분석
    for ac in account_array:
        cnt += 1
        try:
            target_prof = ac
            profile = Profile.from_username(L.context, target_prof)
            posts = profile.get_posts()

            # 게시글 15개 분석 (단, 게시글이 15개 미만일 경우 게시글 수 만큼 분석)
            cnt = 0
            total_likes = 0
            total_comments = 0
            for i in posts:
                cnt += 1
                total_likes += i.likes
                total_comments += i.comments
                if profile.mediacount > 15:
                    if cnt == 15:
                        print(f"계정 분석 완료 : {target_prof}")
                        break
                else:
                    if cnt == profile.mediacount:
                        print(f"계정 분석 완료 : {target_prof}")
                        break

            account = f"https://www.instagram.com/{ac}"
            followers = profile.followers
            avg_likes = total_likes / 15
            avg_comments = total_comments / 15

            final.append({"account": account, "username": target_prof, "followers": format(followers, ","),
                          "avg_likes": round(avg_likes, 2),
                          "avg_comments": round(avg_comments, 2)})
        except:
            except_account = ["아이디", "계정", "계정명"]
            if target_prof not in except_account:
                error_account += 1
                error_account_list.append(ac)
    error_final = {"account": error_account, "list": error_account_list}

    return final, error_final


# 4. (Light버전) 여러 계정 분석하는 함수
def multi_account_check_light(account):
    login_action()

    account_array = account

    # 계정명 오류가 나온 계정에 대한 변수
    error_account = 0
    error_account_list = []
    cnt = 0

    final = []
    # 분석
    for ac in account_array:
        cnt += 1
        try:
            target_prof = ac
            profile = Profile.from_username(L.context, target_prof)

            # 게시글 15개 분석 (단, 게시글이 15개 미만일 경우 게시글 수 만큼 분석)
            cnt = 0
            total_likes = 0
            total_comments = 0

            account = f"https://www.instagram.com/{ac}"
            followers = profile.followers

            final.append({"account": account, "username": target_prof, "followers": format(followers, ",")})
        except:
            except_account = ["아이디", "계정", "계정명"]
            if target_prof not in except_account:
                error_account += 1
                error_account_list.append(ac)
    error_final = {"account": error_account, "list": error_account_list}

    return final, error_final


# 5. 포스팅 분석하기

def posts_check(file):
    login_action()

    posts_array = file
    # 오류가 나온 게시글에 대한 변수
    error_posts = 0
    error_posts_list = []

    final = []
    for post in posts_array:
        target_post = post[28:39]
        try:
            target_post = target_post[-11:]
            ps = Post.from_shortcode(L.context, f'{target_post}')
            target_prof = ps.owner_username
            profile = Profile.from_username(L.context, target_prof)

            final.append({"username": ps.owner_username, "followers": format(profile.followers, ","),
                          "likes": format(ps.likes, ","),
                          "comments": format(ps.comments, ","), "thumbnail": ps.url, "tagged": ps.tagged_users,
                          "upload_date": ps.date_local.strftime("%Y년 %m월 %d일 %H시 %M분")})
        except:
            error_posts += 1
            error_posts_list.append(post)
    error_final = {"count": error_posts, "list": error_posts_list}

    return final, error_final
