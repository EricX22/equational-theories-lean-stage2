% hard3_0092  eq1=707 eq2=4090  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(Y,f(Y,f(f(X,Y),Y))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(f(f(Y,Y),X),X) )).
