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
    greeting varchar(255) NOT NULL,
    icon text(255) NOT NULL
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
INSERT INTO users (uid, username, email, password, address, greeting, icon) VALUES
('1', 'アリス', 'alice@example.com', 'password1', '北海道', 'こんにちは、アリスです。', 'icon1.png'),
('2', 'ボブ', 'bob@example.com', 'password2', '北海道', 'こんにちは、ボブです。', 'icon2.png'),
('3', 'ウィリアムズ', 'williams@example.com', 'password3', '北海道', 'こんにちは、ウィリアムズです。', 'icon3.png'),
('4', 'ブラウン', 'brown@example.com', 'password4', '北海道', 'こんにちは、ブラウンです。', 'icon4.png'),
('5', 'ジョーンズ', 'jones@example.com', 'password5', '北海道', 'こんにちは、ジョーンズです。', 'icon5.png'),
('6', 'ミラー', 'miller@example.com', 'password6', '北海道', 'こんにちは、ミラーです。', 'icon6.png'),
('7', 'デイビス', 'davis@example.com', 'password7', '北海道', 'こんにちは、デイビスです。', 'icon7.png'),
('8', 'ガルシア', 'garcia@example.com', 'password8', '北海道', 'こんにちは、ガルシアです。', 'icon8.png'),
('9', 'マルティネス', 'martinez@example.com', 'password9', '北海道', 'こんにちは、マルティネスです。', 'icon9.png'),
('10', 'ヘルナンデス', 'hernandez@example.com', 'password10', '北海道', 'こんにちは、ヘルナンデスです。', 'icon10.png'),
('11', 'ウィルソン', 'wilson@example.com', 'password12', '青森県', 'こんにちは、ウィルソンです。', 'icon11.png'),
('12', 'ムーア', 'moore@example.com', 'password13', '青森県', 'こんにちは、ムーアです。', 'icon12.png'),
('13', 'テイラー', 'taylor@example.com', 'password14', '青森県', 'こんにちは、テイラーです。', 'icon13.png'),
('14', 'アンダーソン', 'anderson@example.com', 'password15', '青森県', 'こんにちは、アンダーソンです。', 'icon14.png'),
('15', 'トーマス', 'thomas@example.com', 'password16', '青森県', 'こんにちは、トーマスです。', 'icon15.png'),
('16', 'ジャクソン', 'jackson@example.com', 'password17', '青森県', 'こんにちは、ジャクソンです。', 'icon16.png'),
('17', 'ホワイト', 'white@example.com', 'password18', '青森県', 'こんにちは、ホワイトです。', 'icon17.png'),
('18', 'ハリス', 'harris@example.com', 'password19', '青森県', 'こんにちは、ハリスです。', 'icon18.png'),
('19', 'クラーク', 'clark@example.com', 'password20', '青森県', 'こんにちは、クラークです。', 'icon19.png');

-- チャットルームのサンプル挿入
-- INSERT INTO chat (uid, name, abstract, user_ids) VALUES
-- ('1', 'アリスさんとボブさんのチャットルーム', 'アリスさんとボブさんのチャットルームです', '1,2'),
-- ('1', 'アリスさんとチャーリーさんのチャットルーム', 'アリスさんとチャーリーさんのチャットルーム', '1,3');

-- メッセージのサンプル挿入
-- INSERT INTO messages(id, uid, cid, message)VALUES
-- (1, '1', '1', 'こんにちは、佐藤です。名前教えてください！'),
-- (2, '2', '1', 'こんにちは、鈴木です。');