# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_app.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/10 14:06:47 by jmykkane          #+#    #+#              #
#    Updated: 2024/01/10 14:09:39 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from fastapi.testclient import TestClient
from app.main import app

def test_get_restaurants():
	with TestClient(app) as client:
		response = client.get("/restaurants")

		assert response.status_code == 200
		assert len(response.json()) == 20