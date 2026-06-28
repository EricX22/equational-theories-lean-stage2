% hard3_0383  eq1=3972 eq2=4168  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(Y,f(Z,X)),Y) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(f(Y,Y),Y),Y) )).
