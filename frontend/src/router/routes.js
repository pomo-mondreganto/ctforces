const Index = () =>
    import(/* webpackChunkName: "group-main" */ '@/views/Index/Index');
const Login = () =>
    import(/* webpackChunkName: "group-main" */ '@/views/Index/Login');
const Register = () =>
    import(/* webpackChunkName: "group-main" */ '@/views/Index/Register');

const TaskList = () =>
    import(/* webpackChunkName: "group-tasks" */ '@/views/Tasks/List');
const TaskIndex = () =>
    import(/* webpackChunkName: "group-tasks" */ '@/views/Tasks/Index');
const TaskCreate = () =>
    import(/* webpackChunkName: "group-tasks" */ '@/views/Tasks/Create');
const TaskEdit = () =>
    import(/* webpackChunkName: "group-tasks" */ '@/views/Tasks/Edit');
const TaskSolved = () =>
    import(/* webpackChunkName: "group-tasks" */ '@/views/Tasks/Solved');

const ContestCreate = () =>
    import(/* webpackChunkName: "group-contests" */ '@/views/Contests/Create');
const ContestEdit = () =>
    import(/* webpackChunkName: "group-contests" */ '@/views/Contests/Edit');
const ContestIndex = () =>
    import(/* webpackChunkName: "group-contests" */ '@/views/Contests/Index');
const ContestTasks = () =>
    import(
        /* webpackChunkName: "group-contests" */ '@/views/Contests/TaskList'
    );
const ContestScoreboard = () =>
    import(
        /* webpackChunkName: "group-contests" */ '@/views/Contests/Scoreboard'
    );
const ContestTask = () =>
    import(/* webpackChunkName: "group-contests" */ '@/views/Contests/Task');
const ContestTaskSolved = () =>
    import(
        /* webpackChunkName: "group-contests" */ '@/views/Contests/TaskSolved'
    );
const ContestList = () =>
    import(/* webpackChunkName: "group-contests" */ '@/views/Contests/List');
const ContestRegister = () =>
    import(
        /* webpackChunkName: "group-contests" */ '@/views/Contests/Register'
    );
const ContestInfo = () =>
    import(/* webpackChunkName: "group-contests" */ '@/views/Contests/Info');

const Rating = () =>
    import(/* webpackChunkName: "group-main" */ '@/views/Users/Rating');
const Upsolving = () =>
    import(/* webpackChunkName: "group-main" */ '@/views/Users/Upsolving');

const Profile = () =>
    import(/* webpackChunkName: "group-profile" */ '@/views/Users/Profile');
const ProfileMain = () =>
    import(/* webpackChunkName: "group-profile" */ '@/views/Users/ProfileMain');
const ProfileSettings = () =>
    import(
        /* webpackChunkName: "group-profile" */ '@/views/Users/ProfileSettings'
    );
const ProfileBlog = () =>
    import(/* webpackChunkName: "group-profile" */ '@/views/Users/ProfileBlog');
const ProfileTeams = () =>
    import(
        /* webpackChunkName: "group-profile" */ '@/views/Users/ProfileTeams'
    );
const ProfileTasks = () =>
    import(
        /* webpackChunkName: "group-profile" */ '@/views/Users/ProfileTasks'
    );

const PostIndex = () =>
    import(/* webpackChunkName: "group-posts" */ '@/views/Posts/Index');
const PostCreate = () =>
    import(/* webpackChunkName: "group-posts" */ '@/views/Posts/Create');
const PostEdit = () =>
    import(/* webpackChunkName: "group-posts" */ '@/views/Posts/Edit');

const TeamCreate = () =>
    import(/* webpackChunkName: "group-teams" */ '@/views/Teams/Create');
const TeamJoin = () =>
    import(/* webpackChunkName: "group-teams" */ '@/views/Teams/Join');
const TeamIndex = () =>
    import(/* webpackChunkName: "group-teams" */ '@/views/Teams/Index');

const ConfirmEmail = () =>
    import(/* webpackChunkName: "group-main" */ '@/views/Index/ConfirmEmail');
const PasswordReset = () =>
    import(/* webpackChunkName: "group-main" */ '@/views/Index/PasswordReset');
const PasswordResetConfirm = () =>
    import(
        /* webpackChunkName: "group-main" */ '@/views/Index/PasswordResetConfirm'
    );
const EmailResend = () =>
    import(/* webpackChunkName: "group-main" */ '@/views/Index/EmailResend');

const routes = [
    {
        path: '/',
        name: 'index',
        component: Index,
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
    {
        path: '/register',
        name: 'register',
        component: Register,
    },
    {
        path: '/confirm_email',
        name: 'email_confirm',
        component: ConfirmEmail,
    },
    {
        path: '/reset_password',
        name: 'password_reset',
        component: PasswordReset,
    },
    {
        path: '/reset_password_confirm',
        name: 'password_reset_confirm',
        component: PasswordResetConfirm,
    },
    {
        path: '/email_resend',
        name: 'email_resend',
        component: EmailResend,
    },
    {
        path: '/teams/create',
        name: 'team_create',
        component: TeamCreate,
        meta: {
            auth: true,
        },
    },
    {
        path: '/teams/:id/join',
        name: 'team_join',
        component: TeamJoin,
        meta: {
            auth: true,
        },
    },
    {
        path: '/teams/:id',
        name: 'team_index',
        component: TeamIndex,
    },
    {
        path: '/tasks',
        name: 'task_list',
        component: TaskList,
    },
    {
        path: '/tasks/create',
        name: 'task_create',
        component: TaskCreate,
        meta: {
            auth: true,
        },
    },
    {
        path: '/tasks/:id/edit',
        name: 'task_edit',
        component: TaskEdit,
        meta: {
            auth: true,
        },
    },
    {
        path: '/tasks/:id/solved',
        name: 'task_solved',
        component: TaskSolved,
    },
    {
        path: '/tasks/:id',
        name: 'task_index',
        component: TaskIndex,
    },
    {
        path: '/contests/create',
        name: 'contest_create',
        component: ContestCreate,
        meta: {
            auth: true,
        },
    },
    {
        path: '/contests/:id/edit',
        name: 'contest_edit',
        component: ContestEdit,
        meta: {
            auth: true,
        },
    },
    {
        name: 'contest_register',
        path: '/contests/:id/register',
        component: ContestRegister,
        meta: {
            auth: true,
        },
    },
    {
        name: 'contest_scoreboard',
        path: '/contests/:id/scoreboard',
        component: ContestScoreboard,
    },
    {
        path: '/contests/:id',
        component: ContestIndex,

        children: [
            {
                name: 'contest_task_solved',
                path: 'tasks/:task_id/solved',
                component: ContestTaskSolved,
            },
            {
                name: 'contest_task',
                path: 'tasks/:task_id',
                component: ContestTask,
            },
            {
                name: 'contest_tasks',
                path: 'tasks',
                component: ContestTasks,
            },
            {
                name: 'contest_info',
                path: '',
                component: ContestInfo,
            },
        ],
    },
    {
        path: '/contests',
        name: 'contest_list',
        component: ContestList,
    },
    {
        path: '/rating',
        name: 'rating',
        component: Rating,
    },
    {
        path: '/upsolving',
        name: 'upsolving',
        component: Upsolving,
    },
    {
        path: '/users/:username',
        component: Profile,

        children: [
            {
                name: 'profile',
                path: '',
                component: ProfileMain,
            },
            {
                name: 'settings',
                path: 'settings',
                component: ProfileSettings,
                meta: {
                    auth: true,
                },
            },
            {
                name: 'blog',
                path: 'blog',
                component: ProfileBlog,
            },
            {
                name: 'teams',
                path: 'teams',
                component: ProfileTeams,
            },
            {
                name: 'user_tasks',
                path: 'tasks',
                component: ProfileTasks,
            },
        ],
    },
    {
        path: '/posts/create',
        name: 'post_create',
        component: PostCreate,
        meta: {
            auth: true,
        },
    },
    {
        path: '/posts/:id/edit',
        name: 'post_edit',
        component: PostEdit,
        meta: {
            auth: true,
        },
    },
    {
        path: '/posts/:id',
        name: 'post_index',
        component: PostIndex,
    },
];

export default routes;
