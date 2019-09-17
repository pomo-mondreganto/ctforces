const tabs = (username, auth) => {
    if (username && auth) {
        if (auth.loggedIn && username === auth.user.username) {
            const ret = [
                {
                    text: username,
                    href: `/users/${username}`,
                },
            ];

            if (auth.user.has_posts) {
                ret.push({ text: 'Blog', href: `/users/${username}/posts/` });
            }

            if (auth.user.has_tasks) {
                ret.push({ text: 'Tasks', href: `/users/${username}/tasks/` });
            }

            if (auth.user.has_contests) {
                ret.push({ text: 'Contests', href: `/users/${username}/contests/` });
            }

            ret.push({ text: 'General', href: '/settings/general/' });
            ret.push({ text: 'Social', href: '/settings/social/' });

            return ret;
        }
        return [
            {
                text: username,
                href: `/users/${username}`,
            },
            { text: 'Blog', href: `/users/${username}/posts/` },
            { text: 'Tasks', href: `/users/${username}/tasks/` },
            { text: 'Contests', href: `/users/${username}/contests/` },
        ];
    }
    return [];
};

export default tabs;
