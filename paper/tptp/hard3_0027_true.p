% hard3_0027  eq1=134 eq2=176  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Z,X),X)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(Y,Y),f(X,X)) )).
