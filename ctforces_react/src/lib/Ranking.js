function getRank() {
    return 'Master';
}

function getRankColor(rank) {
    if (rank === 'Master') {
        return 'red';
    }
    return 'yellow';
}

export {getRank, getRankColor};
