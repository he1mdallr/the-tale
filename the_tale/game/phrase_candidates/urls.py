# coding: utf-8

from dext.views import resource_patterns


from game.phrase_candidates.views import PhraseCandidateResource

urlpatterns = resource_patterns(PhraseCandidateResource)