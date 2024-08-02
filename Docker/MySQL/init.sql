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
('1', 'アリス', 'alice@example.com', 'password1', '北海道', 'こんにちは、アリスです。'),
('2', 'ボブ', 'bob@example.com', 'password2', '北海道', 'こんにちは、ボブです。'),
('3', 'ウィリアムズ', 'williams@example.com', 'password3', '北海道', 'こんにちは、ウィリアムズです。'),
('4', 'ブラウン', 'brown@example.com', 'password4', '北海道', 'こんにちは、ブラウンです。'),
('5', 'ジョーンズ', 'jones@example.com', 'password5', '北海道', 'こんにちは、ジョーンズです。'),
('6', 'ミラー', 'miller@example.com', 'password6', '北海道', 'こんにちは、ミラーです。'),
('7', 'デイビス', 'davis@example.com', 'password7', '北海道', 'こんにちは、デイビスです。'),
('8', 'ガルシア', 'garcia@example.com', 'password8', '北海道', 'こんにちは、ガルシアです。'),
('9', 'マルティネス', 'martinez@example.com', 'password9', '北海道', 'こんにちは、マルティネスです。'),
('10', 'ヘルナンデス', 'hernandez@example.com', 'password10', '北海道', 'こんにちは、ヘルナンデスです。'),
('11', 'ウィルソン', 'wilson@example.com', 'password12', '青森県', 'こんにちは、ウィルソンです。'),
('12', 'ムーア', 'moore@example.com', 'password13', '青森県', 'こんにちは、ムーアです。'),
('13', 'テイラー', 'taylor@example.com', 'password14', '青森県', 'こんにちは、テイラーです。'),
('14', 'アンダーソン', 'anderson@example.com', 'password15', '青森県', 'こんにちは、アンダーソンです。'),
('15', 'トーマス', 'thomas@example.com', 'password16', '青森県', 'こんにちは、トーマスです。'),
('16', 'ジャクソン', 'jackson@example.com', 'password17', '青森県', 'こんにちは、ジャクソンです。'),
('17', 'ホワイト', 'white@example.com', 'password18', '青森県', 'こんにちは、ホワイトです。'),
('18', 'ハリス', 'harris@example.com', 'password19', '青森県', 'こんにちは、ハリスです。'),
('19', 'クラーク', 'clark@example.com', 'password20', '青森県', 'こんにちは、クラークです。');




-- チャットルームのサンプル挿入
-- INSERT INTO chat (uid, name, abstract, user_ids) VALUES
-- ('1', 'アリスさんとボブさんのチャットルーム', 'アリスさんとボブさんのチャットルームです', '1,2'),
-- ('1', 'アリスさんとチャーリーさんのチャットルーム', 'アリスさんとチャーリーさんのチャットルーム', '1,3');

-- メッセージのサンプル挿入
-- INSERT INTO messages(id, uid, cid, message)VALUES
-- (1, '1', '1', 'こんにちは、佐藤です。名前教えてください！'),
-- (2, '2', '1', 'こんにちは、鈴木です。');