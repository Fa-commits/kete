import { h } from 'preact';
import Message from './Message';

const ChatWindow = ({ messages }) => (
  <div class="chat-window">
    {messages.map(msg => <Message key={msg.id} {...msg} />)}
  </div>
);

export default ChatWindow;