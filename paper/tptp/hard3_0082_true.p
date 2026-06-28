% hard3_0082  eq1=625 eq2=2646  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(X,f(f(Y,Z),X))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(X,X),f(X,Y)),X) )).
