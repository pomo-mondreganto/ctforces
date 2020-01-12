import Index from '@/views/Index';
import Login from '@/views/Login';

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
        component: Index,
    },
];

export default routes;
