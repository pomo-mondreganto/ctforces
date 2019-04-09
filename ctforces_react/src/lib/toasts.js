import 'react-toastify/dist/ReactToastify.css';
import { toast } from 'react-toastify';

const success = text => toast.success(text, {
    position: toast.POSITION.BOTTOM_RIGHT,
    pauseOnHover: false,
});

export { success };
