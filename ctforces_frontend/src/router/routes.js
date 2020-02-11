import Index from '@/views/Index/Index/Index';
import Login from '@/views/Index/Login/Index';
import Register from '@/views/Index/Register/Index';

import TaskList from '@/views/Tasks/List/Index';
import TaskIndex from '@/views/Tasks/Index/Index';
import TaskCreate from '@/views/Tasks/Create/Index';
import TaskEdit from '@/views/Tasks/Edit/Index';

import Rating from '@/views/Users/Rating/Index';
import Upsolving from '@/views/Users/Upsolving/Index';

import Profile from '@/views/Users/Profile/Index';
import ProfileMain from '@/views/Users/Profile/Index/Index';
import ProfileSettings from '@/views/Users/Profile/Settings/Index';

import UserBlog from '@/views/Users/Blog/Index';
import PostIndex from '@/views/Posts/Index/Index';

const routes = [
    {
        path: '/',
        name: 'index',
        component: Index,
    },
    {
        path: '/login/',
        name: 'login',
        component: Login,
    },
    {
        path: '/register/',
        name: 'register',
        component: Register,
    },
    {
        path: '/tasks/',
        name: 'task_list',
        component: TaskList,
    },
    {
        path: '/tasks/create/',
        name: 'task_create',
        component: TaskCreate,
        meta: {
            auth: true,
        },
    },
    {
        path: '/tasks/:id/edit/',
        name: 'task_edit',
        component: TaskEdit,
        meta: {
            auth: true,
        },
    },
    {
        path: '/tasks/:id',
        name: 'task_index',
        component: TaskIndex,
    },
    {
        path: '/rating/',
        name: 'rating',
        component: Rating,
    },
    {
        path: '/upsolving/',
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
            },
            {
                name: 'blog',
                path: 'blog',
                component: UserBlog,
            },
        ],
    },
    {
        path: '/posts/:id',
        name: 'post_index',
        component: PostIndex,
    },
];

export default routes;
