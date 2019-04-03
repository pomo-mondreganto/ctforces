const tabs = username => [
    {
        text: username,
        href: `/users/${username}`,
    },
    { text: 'Blog', href: `/users/${username}/posts/` },
    { text: 'Tasks', href: `/users/${username}/tasks/` },
    { text: 'Contests', href: `/users/${username}/contests/` },
    { text: 'General', href: '/settings/general/' },
    { text: 'Social', href: '/settings/social/' },
];

export default tabs;
