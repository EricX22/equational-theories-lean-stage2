% hard3_0075  eq1=545 eq2=2043  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Z,f(X,f(Z,X)))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(X,X),Y),f(Y,X)) )).
