import React, {Component} from 'react';
import {AdminPage} from '../../../components/admin/AdminPage'


export class MlApiStatsContainer extends Component {
    constructor(props) {
        super(props);

        this.state = {
            styleStats: [
                {
                    "x": "2020-05-16",
                    "y": 3
                },
                {
                    "x": "2020-05-18",
                    "y": 10
                },
                {
                    "x": "2020-05-19",
                    "y": 15
                }
            ],
            usersStats: [
                {
                    "x": "2020-05-16",
                    "y": 2
                },
                {
                    "x": "2020-05-18",
                    "y": 10
                },
                {
                    "x": "2020-05-19",
                    "y": 14
                }
            ],
            stylesList: [
                {
                    id: 1,
                    description: 'Baroque',
                },
                {
                    id: 2,
                    description: 'Renaissance',
                },
                {
                    id: 3,
                    description: 'Modern',
                },
                {
                    id: 4,
                    description: 'Cubism',
                },
                {
                    id: 5,
                    description: 'Graphics',
                },
            ],
            usersList: [
                {
                    id: 1,
                    description: 'Borovyi Orest',
                },
                {
                    id: 2,
                    description: 'Ilechko Roman',
                },
            ],
        };
    };

    render() {
        const {styleStats, stylesList, usersStats, usersList} = this.state;

        return (
            <AdminPage styleStats={styleStats} stylesList={stylesList} usersStats={usersStats} usersList={usersList}/>
        )
    }
};
