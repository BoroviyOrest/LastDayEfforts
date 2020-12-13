import React from 'react';
import {Form, Input, Button, Checkbox} from 'antd';
import {PublicLayout} from '../PublicLayout'
import {UserOutlined, LockOutlined} from '@ant-design/icons';


export const Login = ({onSubmit}) => {
    const layout = {
        wrapperCol: {span: 8, offset: 8},
    };
    return (
        <PublicLayout>
            <Form
                {...layout}
                name="normal_login"
                initialValues={{remember: true}}
                onFinish={onSubmit}
            >
                <Form.Item
                    name="username"
                    rules={[{required: true, message: 'Please input your Username!'}]}
                >
                    <Input prefix={<UserOutlined className="site-form-item-icon"/>} placeholder="Username"/>
                </Form.Item>
                <Form.Item
                    name="password"
                    rules={[{required: true, message: 'Please input your Password!'}]}
                >
                    <Input
                        prefix={<LockOutlined className="site-form-item-icon"/>}
                        type="password"
                        placeholder="Password"
                    />
                </Form.Item>
                <Form.Item>
                    <Form.Item name="remember" valuePropName="checked" noStyle>
                        <Checkbox>Remember me</Checkbox>
                    </Form.Item>
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit" className="login-form-button">
                        Log in
                    </Button>
                    Or <a href="">register now!</a>
                </Form.Item>
            </Form>
        </PublicLayout>
    );
};
