import React, {Component} from 'react';
import {AdminPage} from '../../../components/admin/AdminPage'


export class ClientStatsContainer extends Component {
    constructor(props) {
        super(props);

        this.state = {
            styleStats: [],
            userStats: [],
        };
    };

    render() {
        const {styleStats, userStats} = this.state;

        return (
            <AdminPage styleStats={styleStats} userStats={userStats}/>
        )
    }
};
