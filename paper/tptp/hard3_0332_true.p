% hard3_0332  eq1=3095 eq2=2465  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(f(X,Y),Z),Z),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,f(f(Y,X),Z)),W) )).
