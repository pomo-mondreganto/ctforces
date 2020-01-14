import Index from '@/views/Index';
import Login from '@/views/Login';
import Register from '@/views/Register';

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
];

export default routes;
