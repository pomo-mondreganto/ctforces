import api.models.auxiliary
from api.models.auxiliary import get_anonymous_user_instance
from api.models.objects import (
    User,
    Team,
    Post,
    TaskTag,
    Task,
    TaskHint,
    TaskFile,
    Contest,
)
from api.models.relations import (
    ContestTaskRelationship,
    ContestParticipantRelationship,
    CPRHelper,
)
