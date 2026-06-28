% hard3_0033  eq1=172 eq2=4080  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,X),f(Z,X)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(f(f(Y,X),X),X) )).
