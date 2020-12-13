import React, {Component} from 'react';
import {Registration} from '../../components/Registration';


export class RegistrationContainer extends Component {
    onSubmit = (values) => {
        console.log(values);
    };

    render() {
        return (
            <Registration onSubmit={this.onSubmit}/>
        )
    }
}
