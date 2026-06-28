% hard3_0210  eq1=1970 eq2=2063  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,X)),f(W,X)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(X,Y),Y),f(Y,X)) )).
