% hard3_0299  eq1=2841 eq2=4275  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,U)),X) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(X,X)) = f(Y,f(Y,X)) )).
