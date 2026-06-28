% hard3_0276  eq1=2651 eq2=3933  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,X),f(Y,X)),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(X,f(Y,Z)),W) )).
