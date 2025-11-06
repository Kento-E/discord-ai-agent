import discord
import json
import os
from sentence_transformers import SentenceTransformer, util

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config.json')
EMBED_PATH = os.path.join(os.path.dirname(__file__), '../data/embeddings.json')

with open(CONFIG_PATH, 'r') as f:
	config = json.load(f)

TOKEN = config['DISCORD_TOKEN']
GUILD_ID = int(config['TARGET_GUILD_ID'])

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

client = discord.Client(intents=intents)

# 埋め込みデータロード
if os.path.exists(EMBED_PATH):
	with open(EMBED_PATH, 'r') as f:
		dataset = json.load(f)
	texts = [item['text'] for item in dataset]
	embeddings = [item['embedding'] for item in dataset]
	model = SentenceTransformer('all-MiniLM-L6-v2')

	def search_similar_message(query, top_k=3):
		query_emb = model.encode(query)
		import torch
		scores = util.cos_sim(query_emb, torch.tensor(embeddings))[0]
		top_results = scores.argsort(descending=True)[:top_k]
		return [texts[i] for i in top_results]

@client.event
async def on_ready():
	print(f'Logged in as {client.user}')
	print('Bot is running and ready to answer.')

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	# Botへのメンション or !ask コマンドで応答
	if client.user in message.mentions or message.content.startswith('!ask '):
		query = message.content.replace('!ask ', '').replace(f'<@{client.user.id}>', '').strip()
		if not query:
			await message.channel.send('質問内容を入力してください。')
			return
		if os.path.exists(EMBED_PATH):
			results = search_similar_message(query)
			reply = '過去の類似メッセージ:\n' + '\n'.join(['- ' + r for r in results])
			await message.channel.send(reply)
		else:
			await message.channel.send('知識データが未生成です。まずメッセージ取得・整形を行ってください。')

if __name__ == '__main__':
	client.run(TOKEN)