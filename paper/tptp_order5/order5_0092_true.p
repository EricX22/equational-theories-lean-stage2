% order5_0092  eq1=8417 eq2=21643  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(Y,f(X,f(f(f(X,Y),X),Y))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(X,Z)),f(X,f(Z,X))) )).
