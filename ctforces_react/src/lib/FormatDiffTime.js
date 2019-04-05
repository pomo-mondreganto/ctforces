import moment from 'moment';

export default (time) => {
    let seconds = moment(time).diff(moment(), 'seconds');

    const days = Math.floor(seconds / 60 / 60 / 24).toString();

    seconds -= days * 24 * 60 * 60;

    const hours = Math.floor(seconds / 60 / 60).toString();

    seconds -= hours * 60 * 60;

    const minutes = Math.floor(seconds / 60).toString();

    seconds -= minutes * 60;

    seconds = seconds.toString();

    return `${days} days ${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}:${seconds.padStart(2, '0')}`;
};
