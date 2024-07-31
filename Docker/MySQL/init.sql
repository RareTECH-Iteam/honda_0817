DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    uid varchar(255) PRIMARY KEY,
    username varchar(255) UNIQUE NOT NULL,
    email varchar(255) UNIQUE NOT NULL,
    password varchar(255) NOT NULL,
    address varchar(255) NOT NULL,
    greeting varchar(255) NOT NULL
);

CREATE TABLE chat (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    name varchar(255) UNIQUE NOT NULL,
    abstract varchar(255),
    user_ids text  -- チャットへの権限制御：参加ユーザーのIDをカンマ区切りで保存することにより、1対Nではなく、1対1のチャット
);

CREATE TABLE messages (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    cid integer REFERENCES chat(id) ON DELETE CASCADE,
    message text,
    created_at timestamp not null default current_timestamp
);

-- Create matches table
-- CREATE TABLE matches (
--     match_id serial,
--     user1_id varchar(255) NOT NULL,
--     user2_id varchar(255) NOT NULL,
--     status enum('pending', 'accepted', 'declined') NOT NULL DEFAULT 'pending',
--     PRIMARY KEY (match_id),
--     FOREIGN KEY (user1_id) REFERENCES users(u_id) ON DELETE CASCADE,
--     FOREIGN KEY (user2_id) REFERENCES users(u_id) ON DELETE CASCADE
-- );

-- Create friendRequests table
-- CREATE TABLE friendRequests (
--     request_id serial,
--     from_user_id varchar(255) NOT NULL,
--     to_user_id varchar(255) NOT NULL,
--     status enum('pending', 'accepted', 'declined') NOT NULL DEFAULT 'pending',
--     PRIMARY KEY (request_id),
--     FOREIGN KEY (from_user_id) REFERENCES users(u_id) ON DELETE CASCADE,
--     FOREIGN KEY (to_user_id) REFERENCES users(u_id) ON DELETE CASCADE
-- );

-- ユーザデータのサンプル挿入
INSERT INTO users (uid, username, email, password, address, greeting) VALUES
('1', 'alice', 'alice@example.com', 'password1', '北海道', 'こんにちは、アリスです。'),
('2', 'bob', 'bob@example.com', 'password2', '北海道', 'こんにちは、ボブです。'),
('3', 'charlie', 'charlie@example.com', 'password3', '北海道', 'こんにちは、チャーリーです。'),
('4', 'david', 'david@example.com', 'password4', '北海道', 'こんにちは、デイヴィッドです。'),
('5', 'emma', 'emma@example.com', 'password5', '北海道', 'こんにちは、エマです。'),
('6', 'frank', 'frank@example.com', 'password6', '北海道', 'こんにちは、フランクです。'),
('7', 'grace', 'grace@example.com', 'password7', '北海道', 'こんにちは、グレースです。'),
('8', 'hannah', 'hannah@example.com', 'password8', '北海道', 'こんにちは、ハンナです。'),
('9', 'ian', 'ian@example.com', 'password9', '北海道', 'こんにちは、イアンです。'),
('10', 'julia', 'julia@example.com', 'password10', '北海道', 'こんにちは、ジュリアです。');



-- チャットルームのサンプル挿入
INSERT INTO chat (uid, name, abstract, user_ids) VALUES
('1', 'アリスさんとボブさんのチャットルーム', 'アリスさんとボブさんのチャットルームです', '1,2'),
('1', 'アリスさんとチャーリーさんのチャットルーム', 'アリスさんとチャーリーさんのチャットルーム', '1,3');

-- メッセージのサンプル挿入
INSERT INTO messages(id, uid, cid, message)VALUES
(1, '1', '1', 'こんにちは、アリスです。名前教えてください！');