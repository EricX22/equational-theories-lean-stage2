% hard3_0312  eq1=2896 eq2=55  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,f(Y,Z)),W),Z) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(Y,f(Y,X))) )).
