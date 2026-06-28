% hard3_0112  eq1=906 eq2=1231  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(Y,f(f(Y,X),f(X,X))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(f(f(X,Y),Y),X)) )).
