import 'react-toastify/dist/ReactToastify.css';
import { toast } from 'react-toastify';

const successT = text => toast.success(text, {
    position: toast.POSITION.BOTTOM_RIGHT,
    pauseOnHover: false,
});

const infoT = text => toast.info(text, {
    position: toast.POSITION.BOTTOM_RIGHT,
    pauseOnHover: false,
});

export { successT, infoT };
