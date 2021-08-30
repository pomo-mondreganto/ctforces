import moment from 'moment';

const defaults = {
    id: -1,
    name: '',
    description: '',
    is_published: false,
    is_registration_open: false,
    is_rated: false,
    is_virtual: false,
    virtual_duration: '',
    publish_tasks_after_finished: false,
    public_scoreboard: false,
    dynamic_scoring: false,
    start_time: null,
    end_time: null,
};

class Contest {
    constructor(options) {
        const {
            id,
            name,
            description,
            is_published,
            is_registration_open,
            is_rated,
            is_virtual,
            virtual_duration,
            publish_tasks_after_finished,
            public_scoreboard,
            dynamic_scoring,
            start_time,
            end_time,
        } = { ...defaults, ...options };
        this.id = id;
        this.name = name;
        this.description = description;
        this.is_published = is_published;
        this.is_registration_open = is_registration_open;
        this.is_rated = is_rated;
        this.is_virtual = is_virtual;
        this.virtual_duration = virtual_duration;
        this.publish_tasks_after_finished = publish_tasks_after_finished;
        this.public_scoreboard = public_scoreboard;
        this.dynamic_scoring = dynamic_scoring;
        this.start_time = start_time;
        this.end_time = end_time;
    }

    dumpForAPI() {
        const { ...result } = this;
        result.start_time = moment(result.start_time).toISOString();
        result.end_time = moment(result.end_time).toISOString();
        return result;
    }
}

export default Contest;
