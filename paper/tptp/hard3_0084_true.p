% hard3_0084  eq1=627 eq2=3869  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(X,f(f(Y,Z),Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(f(X,f(Y,X)),Z) )).
