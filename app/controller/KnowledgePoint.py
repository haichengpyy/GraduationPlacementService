from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.models.base import db

from app.models.knowledgePoint import KnowledgePoint
from sqlalchemy import or_, and_, all_, any_

knowledgeBP = Blueprint('knowledge', __name__)
