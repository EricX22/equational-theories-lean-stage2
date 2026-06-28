% hard3_0093  eq1=714 eq2=1075  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(Y,f(Y,f(f(Y,X),Y))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(Y,f(f(X,f(X,Y)),X)) )).
